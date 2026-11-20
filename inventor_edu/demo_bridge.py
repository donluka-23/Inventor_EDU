"""Headless adapter for the owner-frozen HCSR04_GPIO_WIRING scenario."""

from typing import Literal

from .core import compute_nets, resolve_terminal
from .gpio_facts import GpioFactSet
from .gpio_verify import GpioRequirement, GpioVerificationReport, verify_gpio_requirements
from .models import CatalogSnapshot, CircuitSnapshot, Digest, EngineeringModelError, Record, TerminalRef

__all__ = ["analyze_hcsr04_wiring"]

_PROFILES = (
    ("board", "esp32-devkitc-32e-v4", "sha256:8fadb7e6b1c95df25e43a4bd7aaeafd721fd05cc4415e715c5c1ffb60a10d2a9"),
    ("sensor", "adafruit-3942-profile", "sha256:06878d354dc2e3d88a7b0c38c8b39b18f3345c63530a938e3f31e97c70f5bff7"),
)
_SIGNALS = (("TRIG_OUTPUT", "Trig", "GPIO_OUT"), ("ECHO_INPUT", "Echo", "GPIO_IN"))
_CHECKS = ("PIN_MAPPING", "PHYSICAL_CAPABILITY", "BOARD_AVAILABILITY",
           "ACTIVE_CONFIGURATION", "ELECTRICAL_COMPATIBILITY")

_Role = Literal["TRIG_OUTPUT", "ECHO_INPUT"]
_LinkState = Literal["CONNECTED_UNIQUE", "MISSING", "AMBIGUOUS", "NON_GPIO", "SHARED_SIGNAL_NET"]


class DemoLinkResult(Record):
    role: _Role
    sensor_terminal: TerminalRef
    board_terminal: TerminalRef | None
    net_id: str | None
    state: _LinkState


class DemoWiringReport(Record):
    scenario_id: Literal["HCSR04_GPIO_WIRING"] = "HCSR04_GPIO_WIRING"
    scenario_version: Literal["1.0"] = "1.0"
    catalog_digest: Digest
    snapshot_digest: Digest
    factset_digest: Digest
    links: tuple[DemoLinkResult, DemoLinkResult]
    gpio_report: GpioVerificationReport | None
    authorization_scope: Literal["TEST_ONLY_NOT_PRODUCTION"] = "TEST_ONLY_NOT_PRODUCTION"


def _check_profiles(snapshot: CircuitSnapshot) -> None:
    instances = {instance.instance_id: instance for instance in snapshot.instances}
    for instance_id, definition_id, definition_digest in _PROFILES:
        instance = instances.get(instance_id)
        if instance is None:
            raise EngineeringModelError("UNKNOWN_INSTANCE", ("instances",), (instance_id,))
        if (instance.definition_id, instance.definition_digest) != (definition_id, definition_digest):
            raise EngineeringModelError("UNSUPPORTED_DEMO_PROFILE", ("instances", instance_id), (instance_id,))


def _resolve_link(
    catalog: CatalogSnapshot, snapshot: CircuitSnapshot, role: _Role, contact: str,
    net_id: str, members: tuple[str, ...], shared: bool,
) -> DemoLinkResult:
    sensor = TerminalRef(instance_id="sensor", terminal_id=contact)
    board = None
    if shared:
        state = "SHARED_SIGNAL_NET"
    else:
        candidates = tuple(
            TerminalRef(instance_id="board", terminal_id=key.removeprefix("T:board/"))
            for key in members if key.startswith("T:board/")
        )
        gpio = []
        for candidate in candidates:
            mapping = resolve_terminal(catalog, snapshot, candidate).terminal.signal_ref
            if mapping and mapping.target_kind == "soc_gpio" and mapping.mapping_status == "verified":
                gpio.append(candidate)
        if len(gpio) > 1:
            state = "AMBIGUOUS"
        elif not candidates:
            state = "MISSING"
        elif len(gpio) != len(candidates):
            # A non-GPIO board contact on the same net remains an unresolved structure.
            state = "NON_GPIO"
        else:
            state, board = "CONNECTED_UNIQUE", gpio[0]
    return DemoLinkResult(role=role, sensor_terminal=sensor, board_terminal=board, net_id=net_id, state=state)


def analyze_hcsr04_wiring(
    catalog: CatalogSnapshot,
    snapshot: CircuitSnapshot,
    fact_set: GpioFactSet,
    trusted_catalog_sha256: str | None,
    trusted_factset_sha256: str | None,
) -> DemoWiringReport:
    """Resolve the explicit scenario from validated nets and delegate all GPIO checks."""
    topology = compute_nets(catalog, snapshot)
    snapshot = CircuitSnapshot.model_validate(snapshot)
    _check_profiles(snapshot)
    terminal_nets = dict(topology.terminal_to_net)
    members_by_net = {net.net_id: net.members for net in topology.nets}
    trig_net = terminal_nets["T:sensor/Trig"]
    echo_net = terminal_nets["T:sensor/Echo"]
    shared = trig_net == echo_net
    links = (
        _resolve_link(catalog, snapshot, _SIGNALS[0][0], _SIGNALS[0][1],
                      trig_net, members_by_net[trig_net], shared),
        _resolve_link(catalog, snapshot, _SIGNALS[1][0], _SIGNALS[1][1],
                      echo_net, members_by_net[echo_net], shared),
    )
    requests = tuple(
        GpioRequirement(
            requirement_id=link.role, terminal=link.board_terminal, requested_function=function,
            checks=_CHECKS, operating_state="ACTIVE",
        )
        for link, (_, _, function) in zip(links, _SIGNALS, strict=True) if link.board_terminal is not None
    )
    # Even an empty request list takes the existing pin and fact-set validation path.
    gpio_report = verify_gpio_requirements(
        catalog, snapshot, fact_set, requests, trusted_catalog_sha256, trusted_factset_sha256,
    )
    return DemoWiringReport(
        catalog_digest=gpio_report.catalog_digest, snapshot_digest=topology.snapshot_sha256,
        factset_digest=gpio_report.factset_digest, links=links, gpio_report=gpio_report if requests else None,
    )
