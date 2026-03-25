# TESLA Core Protocol - Primitive: Observation
# Version: 0.1
# Status: Extracted from monolithic models.py (no behavior changes)
#
# Observation is the atomic unit of truth in the TESLA Core Protocol.
# It enforces structural identity, temporal validity, source–origin coherence,
# content integrity, and global uniqueness of observation IDs.

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, PrivateAttr
from datetime import datetime, timedelta
from typing import Literal, ClassVar

from .provenance import Provenance


class Observation(BaseModel):
    """
    Observation represents a single truth-bearing event in the TESLA protocol.

    Invariants enforced:
    - id:
        - starts with 'obs_'
        - suffix contains only lowercase letters, digits, underscores
        - max length 64
        - globally unique across all Observations
    - timestamp:
        - datetime object (strict)
        - timezone-naive
        - not before Unix epoch
        - not more than 1 second in the future
    - source:
        - one of: user, tool, memory, environment, system
    - content:
        - non-empty UTF-8 string
        - max length 10,000 characters
    - provenance:
        - must match source-origin rules
    """

    model_config = ConfigDict(
        strict=True,
        validate_default=True,
        validate_assignment=True,
        from_attributes=True,
    )

    # Global registry of used Observation IDs
    _used_ids: ClassVar[set[str]] = set()
    _id_checked: bool = PrivateAttr(default=False)

    id: str
    timestamp: datetime
    source: Literal["user", "tool", "memory", "environment", "system"]
    content: str
    provenance: Provenance

    @field_validator("timestamp")
    def enforce_timestamp_not_in_future(cls, v):
        if v.tzinfo is not None:
            raise ValueError("timestamp must be timezone-naive (no tzinfo)")
        
        if v > datetime.utcnow() + timedelta(seconds=1):
            raise ValueError("timestamp cannot be more than 1 second in the future")

        
        unix_epoch = datetime(1970, 1, 1)
        if v < unix_epoch:
            raise ValueError("timestamp cannot be before the Unix epoch (1970-01-01)")
        
        return v

    @field_validator("timestamp", mode="before")
    def enforce_strict_timestamp(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("timestamp must be a datetime object (strict mode)")
        return v

    @field_validator("id")
    def enforce_obs_prefix(cls, v):
        if not v.startswith("obs_"):
            raise ValueError("id must start with 'obs_'")
        return v

    @field_validator("content")
    def enforce_non_empty_content(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("content must not be empty")
        try:
            v.encode("utf-8")
        except UnicodeEncodeError:
            raise ValueError("content must be valid UTF-8")
        if len(v) > 10000:
            raise ValueError("content must not exceed 10,000 characters")
        return v

    @model_validator(mode="after")
    def enforce_source_origin_consistency(self):
        if self.source == "memory":
            if self.provenance.origin not in {"memory", "system"}:
                raise ValueError(
                    "If source is 'memory', provenance.origin must be 'memory' or 'system'"
                )
        if self.source == "tool":
            if self.provenance.origin != "tool":
                raise ValueError(
                    "If source is 'tool', provenance.origin must match 'tool'"
                )
        if self.source == "environment":
            if self.provenance.origin not in {"sensor", "environment"}:
                raise ValueError(
                    "If source is 'environment', provenance.origin must be 'sensor' or 'environment'"
                )
        if self.source == "system":
            if self.provenance.origin != "system":
                raise ValueError(
                    "If source is 'system', provenance.origin must be 'system'"
                )
        if self.source == "user":
            if self.provenance.origin != "user":
                raise ValueError(
                    "If source is 'user', provenance.origin must be 'user'"
                )
        return self

    @model_validator(mode="after")
    def enforce_unique_id(self):
        if not self._id_checked:
            if self.id in Observation._used_ids:
                raise ValueError(f"Observation id '{self.id}' must be unique")
            Observation._used_ids.add(self.id)
            self._id_checked = True
        return self

    @field_validator("id")
    def enforce_obs_prefix_and_well_formed(cls, v):
        if not v.startswith("obs_"):
            raise ValueError("id must start with 'obs_'")
        if len(v) > 64:
            raise ValueError("id must not exceed 64 characters")
        suffix = v[len("obs_"):]
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        if not suffix:
            raise ValueError("id must have characters after 'obs_'")
        if not all(c in allowed for c in suffix):
            raise ValueError("id suffix must contain only lowercase letters, digits, or underscores")
        return v