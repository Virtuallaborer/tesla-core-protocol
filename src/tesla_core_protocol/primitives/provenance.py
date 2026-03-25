# TESLA Core Protocol - Primitive: Provenance
# Version: 0.1
# Status: Extracted from monolithic models.py (no behavior changes)
#
# Provenance is the truth-preserving metadata attached to every Observation.
# It enforces structural identity, origin coherence, and calibrated confidence.

from pydantic import BaseModel, ConfigDict, field_validator


class Provenance(BaseModel):
    """
    Provenance captures the truth-preserving metadata for an Observation.

    Invariants:
    - hash:
        - non-empty string
        - lowercase hexadecimal
        - length between 32 and 256 characters
    - origin:
        - non-empty string
        - lowercase
        - characters limited to [a-z0-9_]
    - confidence:
        - float between 0.0 and 1.0 inclusive
    """

    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
    )

    hash: str
    origin: str
    confidence: float

    @field_validator("confidence")
    def enforce_confidence_range(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("confidence must be between 0 and 1")
        return v

    @field_validator("hash")
    def enforce_hash_well_formed(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("hash must be a non-empty string")

        if len(v) < 32:
            raise ValueError("hash must be at least 32 hexadecimal characters")

        if len(v) > 256:
            raise ValueError("hash must not exceed 256 characters")

        if not all(c in "0123456789abcdef" for c in v.lower()):
            raise ValueError("hash must contain only lowercase hexadecimal characters")

        return v

    @field_validator("origin")
    def enforce_origin_well_formed(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("origin must be a non-empty string")

        if v != v.lower():
            raise ValueError("origin must be lowercase")

        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        if not all(c in allowed for c in v):
            raise ValueError("origin must contain only lowercase letters, digits, or underscores")

        return v