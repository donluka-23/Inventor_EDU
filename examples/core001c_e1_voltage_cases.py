"""Show exact test-only divider calculations and their unresolved evidence scopes."""

import argparse
from decimal import Decimal
import json

from examples.edu001_learning_cycle import load_fixture
from inventor_edu.core import create_snapshot
from inventor_edu.models import Conductor, TerminalRef
from inventor_edu.voltage_model import (
    AssumptionRecord, IdealDividerHypothesis, ResistanceInterval, SnapshotAssociation,
    ThresholdHypothesis, VoltageInterval, evaluate_ideal_divider,
)

D = Decimal


def fixture_association() -> SnapshotAssociation:
    catalog, _, instances = load_fixture()
    snapshot = create_snapshot(catalog, instances=instances, junctions=(), conductors=tuple(
        Conductor(connection_id=key, endpoint_a=TerminalRef(instance_id="sensor", terminal_id=source),
                  endpoint_b=TerminalRef(instance_id="board", terminal_id=target))
        for key, source, target in (("syn-TRIG_OUTPUT", "Trig", "J3.9"), ("syn-ECHO_INPUT", "Echo", "J3.8"))
    ))
    return SnapshotAssociation.from_core(catalog, snapshot)


def fixture_cases() -> tuple[IdealDividerHypothesis, ...]:
    association = fixture_association()
    static = (
        AssumptionRecord(record_id="ideal-scope", provenance="MODEL_ASSUMPTION",
            description="Ideal DC unloaded two-resistor divider with independent parameters.",
            condition="Output load absent in the model. Source voltage means voltage applied at the top resistor."),
        AssumptionRecord(record_id="resistors", provenance="MODEL_ASSUMPTION",
            description="Resistor values and tolerance are hypothetical inputs.",
            condition="These proposed components are outside the associated physical netlist."),
        AssumptionRecord(record_id="threshold", provenance="MODEL_ASSUMPTION",
            description="Illustrative 0.75 × 3.4 V = 2.55 V model requirement.",
            condition="A comparator hypothesis. Applicability to a specific receiver is unestablished."),
        AssumptionRecord(record_id="retail-context", provenance="RETAILER_DESCRIPTION",
            description="Seller describes the Echo signal as 5 V logic.",
            condition="Retail context only. It establishes no maker VOH_min or VOL_max envelope.",
            source_ref="https://www.adafruit.com/product/3942", revision="Product 3942 listing",
            locator="Description; Technical Details (Research C S03)"),
        AssumptionRecord(record_id="supply-context", provenance="MANUFACTURER_DOCUMENT",
            description="Module supply absolute-maximum entry concerns VDD33.",
            condition="Context only. No GPIO input stress limit is admitted.",
            source_ref="https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html",
            revision="v2.1 (Research C S01)", locator="Section 6.1, Table 13"),
    )
    cases = []
    for name, vin_low, vin_high, top, tolerance in (
        ("nominal-equal", "5", "5", "10", "0"),
        ("nominal-6k8-top", "5", "5", "6.8", "0"),
        ("interval-6k8-top", "4.5", "5.25", "6.8", "1"),
    ):
        cases.append(IdealDividerHypothesis(
            hypothesis_id=name, scope="IDEAL_DC_UNLOADED_2R", model_assumption_id="ideal-scope",
            parameter_relationship="INDEPENDENT", association=association,
            input_voltage=VoltageInterval(lower=D(vin_low), upper=D(vin_high), unit="V", assumption_id="input"),
            r_top=ResistanceInterval(lower=D(top), upper=D(top), unit="kΩ",
                                      tolerance_percent=D(tolerance), assumption_id="resistors"),
            r_bottom=ResistanceInterval(lower=D("10"), upper=D("10"), unit="kΩ",
                                         tolerance_percent=D(tolerance), assumption_id="resistors"),
            threshold=ThresholdHypothesis(
                required_high=VoltageInterval(lower=D("2.55"), upper=D("2.55"), unit="V", assumption_id="threshold"),
            ),
            assumptions=(*static, AssumptionRecord(record_id="input", provenance="MODEL_ASSUMPTION",
                description=f"Hypothetically applied input interval [{vin_low}, {vin_high}] V.",
                condition="Input is stipulated for the calculation. No source-drive, load or waveform guarantee.")),
        ))
    return tuple(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit deterministic UTF-8 JSON")
    args = parser.parse_args()
    reports = tuple(evaluate_ideal_divider(case) for case in fixture_cases())
    if args.json:
        print(json.dumps([report.model_dump(mode="json") for report in reports],
                         ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return
    for report in reports:
        result = report.calculation
        out = result.output_voltage
        margin = next(row for row in report.findings if row.rule_id == "MODEL_HIGH_MARGIN")
        print(f"{report.hypothesis.hypothesis_id} | {report.restriction} | {report.qualification} | {report.calculation_digest}")
        print(f"  Vout [{out.lower.decimal_12dp}, {out.upper.decimal_12dp}] V | "
              f"HIGH margin {result.high_margin.decimal_12dp} V | {margin.qualification} | {margin.status}")
    print(f"  {reports[0].explanation_code} | physical_network_provenance={reports[0].physical_network_provenance}")
    print("  The resistors are hypothesized. The associated CORE snapshot contains the fixture wiring.")
    for row in reports[0].findings[2:]:
        print(f"  {row.rule_id}={row.status} | {', '.join(row.missing_prerequisites)}")


if __name__ == "__main__":
    main()
