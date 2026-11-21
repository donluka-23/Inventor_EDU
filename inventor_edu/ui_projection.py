"""Read-only projection of native GPIO results for one canonical terminal."""

from collections import Counter as _Counter, defaultdict as _defaultdict
from typing import Annotated as _Annotated, Literal as _Literal

from pydantic import Field as _Field, ValidationError as _ValidationError

from .gpio_facts import canonical_json as _canonical_json
from .gpio_verify import (
    GpioCoverage as _GpioCoverage,
    GpioFinding as _GpioFinding,
    GpioVerificationReport as _GpioVerificationReport,
)
from .models import Digest as _Digest, Record as _Record
from .models import TerminalRef as _TerminalRef, TopologyResult as _TopologyResult

__all__ = [
    "ProjectionInputError",
    "GpioFindingProjectionItem",
    "GpioCoverageProjectionItem",
    "GpioTerminalInspection",
    "project_gpio_terminal",
    "serialize_gpio_terminal_inspection",
]


class ProjectionInputError(ValueError):
    """The supplied inputs cannot produce a consistent inspection."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class GpioFindingProjectionItem(_Record):
    kind: _Literal["GPIO_FINDING"] = "GPIO_FINDING"
    record: _GpioFinding


class GpioCoverageProjectionItem(_Record):
    kind: _Literal["GPIO_COVERAGE"] = "GPIO_COVERAGE"
    record: _GpioCoverage


class GpioTerminalInspection(_Record):
    schema_version: _Literal["ux08-t02a-v1"] = "ux08-t02a-v1"
    terminal: _TerminalRef
    net_id: str
    net_members: tuple[str, ...]
    snapshot_digest: _Digest
    catalog_digest: _Digest
    factset_digest: _Digest
    ruleset_version: _Literal["gpio-capability-v1"]
    records: tuple[_Annotated[
        GpioFindingProjectionItem | GpioCoverageProjectionItem, _Field(discriminator="kind")
    ], ...]


def _terminal_key(terminal: _TerminalRef) -> str:
    return f"T:{terminal.instance_id}/{terminal.terminal_id}"


def _check_topology(topology, selected, record_keys):
    terminal_nets = _defaultdict(list)
    mapped_members = _defaultdict(set)
    for key, net_id in topology.terminal_to_net:
        terminal_nets[key].append(net_id)
        mapped_members[net_id].add(key)
    if selected not in terminal_nets:
        raise ProjectionInputError("PROJECTION_TERMINAL_NOT_IN_TOPOLOGY")

    net_members = _defaultdict(list)
    membership_count = _Counter()
    for net in topology.nets:
        net_members[net.net_id].append(net.members)
        membership_count.update(net.members)

    checked_nets = {}
    # An absent report terminal is a record error. Check all available topology
    # first so a broken net takes precedence over any report inconsistency.
    for key in ({selected} | record_keys) & terminal_nets.keys():
        matches = terminal_nets[key]
        if len(matches) != 1 or not matches[0].strip():
            raise ProjectionInputError("PROJECTION_INCONSISTENT_TOPOLOGY")
        net_id = matches[0]
        if net_id in checked_nets:
            continue
        nets = net_members.get(net_id, ())
        if len(nets) != 1:
            raise ProjectionInputError("PROJECTION_INCONSISTENT_TOPOLOGY")
        members = nets[0]
        if (set(members) != mapped_members[net_id] or
                any(terminal_nets[member] != [net_id] or membership_count[member] != 1
                    for member in members)):
            raise ProjectionInputError("PROJECTION_INCONSISTENT_TOPOLOGY")
        checked_nets[net_id] = members

    return terminal_nets, checked_nets


def project_gpio_terminal(
    topology: _TopologyResult,
    report: _GpioVerificationReport,
    terminal: _TerminalRef,
) -> GpioTerminalInspection:
    """Select a terminal's net and native records after validating the inputs."""
    if (type(topology) is not _TopologyResult or type(report) is not _GpioVerificationReport or
            type(terminal) is not _TerminalRef):
        raise ProjectionInputError("PROJECTION_INVALID_INPUT")
    try:
        topology = _TopologyResult.model_validate(topology, strict=True)
        report = _GpioVerificationReport.model_validate(report, strict=True)
        terminal = _TerminalRef.model_validate(terminal, strict=True)
    except _ValidationError:
        raise ProjectionInputError("PROJECTION_INVALID_INPUT") from None

    if topology.snapshot_sha256 != report.snapshot_digest:
        raise ProjectionInputError("PROJECTION_SNAPSHOT_MISMATCH")
    selected = _terminal_key(terminal)
    native_records = report.findings + report.coverage
    terminal_nets, net_members = _check_topology(
        topology, selected, {_terminal_key(record.terminal) for record in native_records},
    )

    for record in native_records:
        if (record.snapshot_digest != report.snapshot_digest or
                record.catalog_digest != report.catalog_digest or
                record.factset_digest != report.factset_digest or
                terminal_nets.get(_terminal_key(record.terminal)) != [record.affected_net]):
            raise ProjectionInputError("PROJECTION_INCONSISTENT_NATIVE_RECORD")

    if len({record.finding_id for record in native_records}) != len(native_records):
        raise ProjectionInputError("PROJECTION_DUPLICATE_RECORD_ID")

    records = [
        GpioFindingProjectionItem(record=record)
        for record in report.findings if record.terminal == terminal
    ] + [
        GpioCoverageProjectionItem(record=record)
        for record in report.coverage if record.terminal == terminal
    ]
    records.sort(key=lambda item: (
        item.record.requirement_id, item.record.rule_id, item.kind, item.record.finding_id,
    ))
    net_id = terminal_nets[selected][0]
    return GpioTerminalInspection(
        terminal=terminal, net_id=net_id, net_members=net_members[net_id],
        snapshot_digest=report.snapshot_digest, catalog_digest=report.catalog_digest,
        factset_digest=report.factset_digest, ruleset_version=report.ruleset_version,
        records=tuple(records),
    )


def serialize_gpio_terminal_inspection(value: GpioTerminalInspection) -> bytes:
    """Serialize an inspection with the native canonical JSON policy."""
    return _canonical_json(value.model_dump(mode="json"))
