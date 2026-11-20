"""Headless INVENTOR EDU connectivity core."""

from .core import (
    compute_nets, create_snapshot, load_catalog, resolve_terminal,
    restore_snapshot, serialize_snapshot, serialize_topology,
)
from .gpio_facts import GpioFactSet, GpioVerificationError, load_gpio_factset
from .gpio_verify import GpioRequirement, GpioVerificationReport, serialize_gpio_report, verify_gpio_requirements
from .models import (
    CatalogSnapshot, CircuitSnapshot, ComponentInstance, Conductor, DeviceDefinition,
    DeviceIdentity, EngineeringModelError, EvidenceClaim, InternalIdealTie, Junction,
    JunctionRef, ResolvedTerminal, SignalMapping, SignalMappingEvidence, SourceDocument, TerminalDefinition,
    TerminalRef, TopologyResult,
)

__all__ = [
    "GpioFactSet", "GpioRequirement", "GpioVerificationError", "GpioVerificationReport",
    "load_gpio_factset", "serialize_gpio_report", "verify_gpio_requirements",
    "compute_nets", "create_snapshot", "load_catalog", "resolve_terminal",
    "restore_snapshot", "serialize_snapshot", "serialize_topology",
    "CatalogSnapshot", "CircuitSnapshot", "ComponentInstance", "Conductor",
    "DeviceDefinition", "DeviceIdentity", "EngineeringModelError", "EvidenceClaim",
    "InternalIdealTie", "Junction", "JunctionRef", "ResolvedTerminal", "SignalMapping",
    "SignalMappingEvidence", "SourceDocument", "TerminalDefinition", "TerminalRef", "TopologyResult",
]
