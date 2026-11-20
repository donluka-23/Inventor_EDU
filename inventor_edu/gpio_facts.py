"""Typed, digest-pinned GPIO evidence, separate from the circuit catalog."""

from hashlib import sha256
import json
from typing import Literal

from pydantic import ValidationError

from .models import Digest, Identifier, Nonempty, Record


class GpioVerificationError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class HardwareScope(Record):
    definition_id: Identifier
    definition_digest: Digest
    board_family: Nonempty
    board_revision: Nonempty
    orderable_part: Nonempty
    module: Nonempty
    silicon: Nonempty
    profile_scope: Nonempty


class GpioSource(Record):
    source_id: Identifier
    url: Nonempty
    revision: Nonempty
    artifact_sha256: Digest
    rights: Nonempty


class SourceFact(Record):
    claim_id: Identifier
    target: Identifier
    source_ids: tuple[Identifier, ...]
    locator: Nonempty
    review: Literal["approved", "unverified", "conflicting"]


class MappingFact(SourceFact):
    terminal_id: Identifier


class SiliconFact(SourceFact):
    silicon: Nonempty
    input_allowed: bool | None = None
    output_allowed: bool | None = None
    pullup_allowed: bool | None = None


class BoardResourceFact(SourceFact):
    operating_state: Identifier
    reservation: Literal["reserved", "available", "unknown"]
    reason: Nonempty


class StrapFact(SourceFact):
    is_strapping: bool
    boot_state: Identifier
    condition: Nonempty
    prerequisites: tuple[Identifier, ...]


class GpioFactSet(Record):
    schema_version: Literal["1.0"]
    catalog_digest: Digest
    factset_digest: Digest
    scope: HardwareScope
    review: Literal["TEST_ONLY_SOURCE_REVIEWED", "TEST_ONLY_SYNTHETIC", "UNREVIEWED"]
    sources: tuple[GpioSource, ...]
    mappings: tuple[MappingFact, ...]
    silicon: tuple[SiliconFact, ...]
    resources: tuple[BoardResourceFact, ...]
    straps: tuple[StrapFact, ...]


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def factset_digest(fact_set: GpioFactSet) -> str:
    """Hash sorted fact/source records, excluding the root digest itself."""
    body = fact_set.model_dump(mode="json", exclude={"factset_digest"})
    body["sources"].sort(key=lambda item: item["source_id"])
    for field in ("mappings", "silicon", "resources", "straps"):
        body[field].sort(key=lambda item: item["claim_id"])
        for item in body[field]:
            item["source_ids"].sort()
            if field == "straps":
                item["prerequisites"].sort()
    return digest_bytes(canonical_json(body))


def validate_factset(value: GpioFactSet) -> GpioFactSet:
    try:
        facts = GpioFactSet.model_validate(value)
    except ValidationError as exc:
        raise GpioVerificationError("INVALID_FACTSET") from exc
    sources = {source.source_id for source in facts.sources}
    rows = (*facts.mappings, *facts.silicon, *facts.resources, *facts.straps)
    if (len(sources) != len(facts.sources) or len({row.claim_id for row in rows}) != len(rows)
            or any(not row.source_ids or not set(row.source_ids) <= sources for row in rows)
            or any(row.silicon != facts.scope.silicon for row in facts.silicon)):
        raise GpioVerificationError("INVALID_FACTSET")
    if factset_digest(facts) != facts.factset_digest:
        raise GpioVerificationError("FACTSET_DIGEST_MISMATCH")
    return facts


def load_gpio_factset(payload: bytes) -> GpioFactSet:
    if type(payload) is not bytes or len(payload) > 1024 * 1024:
        raise GpioVerificationError("INVALID_FACTSET")

    def unique(pairs):
        result = dict(pairs)
        if len(result) != len(pairs):
            raise ValueError("duplicate JSON key")
        return result

    try:
        json.loads(payload.decode("utf-8"), object_pairs_hook=unique)
        facts = GpioFactSet.model_validate_json(payload)
    except (ValueError, RecursionError) as exc:
        raise GpioVerificationError("INVALID_FACTSET") from exc
    return validate_factset(facts)
