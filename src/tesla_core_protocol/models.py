# TESLA Core Protocol - Primitive 1: Observation
# Version: 0.1
# Status: Skeleton (no logic yet)

# This file will define the Observation primitive.
# We will add fields only after confirming the structure and error protocol.

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, PrivateAttr
from typing import Literal
from datetime import datetime, timedelta
from typing import Any
from pydantic import ValidationError
from typing import Literal, Any, ClassVar


#PROVENANCE BASE MODEL

class Provenance(BaseModel):
    model_config = ConfigDict(
        strict=True,
        from_attributes=True
    )

    hash: str
    origin: str
    confidence: float

    @field_validator("confidence")
    def enforce_confidence_range(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("confidence must be between 0 and 1")
        return v
    
    @field_validator("hash")
    def enforce_hash_well_formed(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("hash must be a non-empty string")
        
        # New rule: minimum length 32 characters
        if len(v) < 32:
            raise ValueError("hash must be at least 32 hexadecimal characters")
        
        # New rule: maximum length 256 characters
        if len(v) > 256:
            raise ValueError("hash must not exceed 256 characters")

        # Minimal well-formed rule: lowercase hex only
        if not all(c in "0123456789abcdef" for c in v.lower()):
            raise ValueError("hash must contain only lowercase hexadecimal characters")

        return v

    @field_validator("origin")
    def enforce_origin_well_formed(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("origin must be a non-empty string")

        # Must be lowercase
        if v != v.lower():
            raise ValueError("origin must be lowercase")

        # Allowed characters: a–z, 0–9, underscore
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        if not all(c in allowed for c in v):
            raise ValueError("origin must contain only lowercase letters, digits, or underscores")

        return v

#OBSERVATION BASE MODEL

class Observation(BaseModel):
    model_config = ConfigDict(
        strict=True,
        validate_default=True,
        validate_assignment=True,
        from_attributes=True,
    )

    # Class-level registry of used IDs
    _used_ids: ClassVar[set[str]] = set()

    # Per-instance flag to avoid re-enforcing uniqueness on the same object
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
        # Only enforce uniqueness the first time this instance is validated
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
    
from pydantic import Field

#ObservationStreamBaseModel BEGIN---
  
class ObservationStream(BaseModel):
    model_config = ConfigDict(
        strict=True,
        validate_default=False,   # ← prevents re-validation of Observation
        validate_assignment=True,
        from_attributes=True,
        revalidate_instances="never",
    )

    id: str
    observations: list[Observation] = Field(..., validate_default=False)
    _used_stream_ids: ClassVar[set[str]] = set() 
    _id_checked: bool = PrivateAttr(default=False)

    @model_validator(mode="after")
    def enforce_non_empty_stream(self):
        if not self.observations:
            raise ValueError("ObservationStream must contain at least one Observation")
        return self



    @model_validator(mode="after")
    def enforce_monotonic_timestamps(self):
        # No observations → nothing to validate
        if not self.observations:
            return self

        # Extract timestamps
        timestamps = [obs.timestamp for obs in self.observations]

        # Enforce strictly increasing timestamps
        for i in range(1, len(timestamps)):
            if timestamps[i] <= timestamps[i - 1]:
                raise ValueError(
                    f"Observation at index {i} has timestamp {timestamps[i]} "
                    f"which is not strictly greater than previous timestamp {timestamps[i - 1]}"
                )

        return self
    
    @model_validator(mode="after")
    def enforce_strictly_increasing_observation_ids(self):
        if len(self.observations) < 2:
            return self

        ids = [obs.id for obs in self.observations]

        for i in range(1, len(ids)):
            if ids[i] <= ids[i - 1]:
                raise ValueError(
                    f"Observation id '{ids[i]}' at index {i} must be strictly greater than "
                    f"previous id '{ids[i - 1]}'"
                )

        return self
    
    @model_validator(mode="after")
    def enforce_strictly_increasing_provenance_hashes(self):
        if len(self.observations) < 2:
            return self

        hashes = [obs.provenance.hash for obs in self.observations]

        for i in range(1, len(hashes)):
            if hashes[i] < hashes[i - 1]:
                raise ValueError(
            f"Provenance hash '{hashes[i]}' at index {i} must not be less than "
            f"previous hash '{hashes[i - 1]}'"
        )


        return self
    
    @model_validator(mode="after")
    def enforce_non_decreasing_provenance_confidence(self):
        if len(self.observations) < 2:
            return self

        confidences = [obs.provenance.confidence for obs in self.observations]

        for i in range(1, len(confidences)):
            if confidences[i] < confidences[i - 1]:
                raise ValueError(
                    f"Provenance confidence {confidences[i]} at index {i} must not be less than "
                    f"previous confidence {confidences[i - 1]}"
                )

        return self
    
    @model_validator(mode="after")
    def enforce_provenance_origin_coherence(self):
        if len(self.observations) < 2:
            return self

        origins = [obs.provenance.origin for obs in self.observations]
        first = origins[0]

        for i, origin in enumerate(origins[1:], start=1):
            if origin != first:
                raise ValueError(
                    f"Provenance origin '{origin}' at index {i} does not match "
                    f"stream origin '{first}'"
                )

        return self


    @model_validator(mode="after")
    def enforce_source_adjacency(self):
        # No adjacency to check if fewer than 2 observations
        if len(self.observations) < 2:
            return self

        for prev, curr in zip(self.observations, self.observations[1:]):
        # Minimal rule for Invariant 4.1:
        # Reject system → user transitions
                        # Invariant 4.2:
        # Reject environment → memory transitions
                        # Invariant 4.3:
        # Reject user → tool transitions
                        # Invariant 4.4:
        # Reject tool → memory transitions
                        # Invariant 4.5:
        # Reject system → memory transitions
                # Invariant 4.6:
        # Reject memory → system transitions
                # Invariant 4.7:
        # Reject tool → system transitions
                # Invariant 4.8:
        # Reject environment → system transitions
                # Invariant 4.9:
        # Reject user → system transitions
                # Invariant 4.10:
        # Reject memory → user transitions
                # Invariant 4.11:
        # Reject tool → user transitions
                # Invariant 4.12:
        # Reject memory → tool transitions
                # Invariant 4.13:
        # Reject memory → environment transitions
                # Invariant 4.15:
        # Reject tool → environment transitions
            if prev.source == "tool" and curr.source == "environment":
                raise ValueError(
                    "Invalid source transition: tool → environment"
            )
        
            if prev.source == "memory" and curr.source == "environment":
                raise ValueError(
                    "Invalid source transition: memory → environment"
            )

            if prev.source == "memory" and curr.source == "tool":
                raise ValueError(
                    "Invalid source transition: memory → tool"
            )

            if prev.source == "tool" and curr.source == "user":
                raise ValueError(
                    "Invalid source transition: tool → user"
            )

            if prev.source == "memory" and curr.source == "user":
                raise ValueError(
                    "Invalid source transition: memory → user"
            )

            if prev.source == "user" and curr.source == "system":
                raise ValueError(
                "Invalid source transition: user → system"
            )

            if prev.source == "environment" and curr.source == "system":
                raise ValueError(
                "Invalid source transition: environment → system"
            )

            if prev.source == "tool" and curr.source == "system":
                raise ValueError(
                "Invalid source transition: tool → system"
            )

            if prev.source == "memory" and curr.source == "system":
                raise ValueError(
                "Invalid source transition: memory → system"
            )

            if prev.source == "system" and curr.source == "memory":
                raise ValueError(
                "Invalid source transition: system → memory"
            )

            if prev.source == "tool" and curr.source == "memory":
                raise ValueError(
                "Invalid source transition: tool → memory"
            )

            if prev.source == "user" and curr.source == "tool":
                raise ValueError(
                "Invalid source transition: user → tool"
            )

            if prev.source == "environment" and curr.source == "memory":
                raise ValueError(
                    "Invalid source transition: environment → memory"
                )

            if prev.source == "system" and curr.source == "user":
                raise ValueError(
                    "Invalid source transition: system → user"
                )
            

        return self
    
    
    @field_validator("id")
    def enforce_stream_id_well_formed(cls, v):
        if not isinstance(v, str):
            raise ValueError("stream id must be a string")

        if not v.startswith("stream_"):
            raise ValueError("stream id must start with 'stream_'")

        suffix = v[len("stream_"):]
        if not suffix:
            raise ValueError("stream id must have characters after 'stream_'")

        if len(v) > 64:
            raise ValueError("stream id must not exceed 64 characters")

        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        if not all(c in allowed for c in suffix):
            raise ValueError("stream id suffix must contain only lowercase letters, digits, or underscores")

        return v
    
    @model_validator(mode="after")
    def enforce_unique_stream_id(self):
        if not self._id_checked:
            if self.id in ObservationStream._used_stream_ids:
                raise ValueError(f"ObservationStream id '{self.id}' must be unique")
            ObservationStream._used_stream_ids.add(self.id)
            self._id_checked = True

        return self
    
    @model_validator(mode="after")
    def enforce_temporal_gap_limit(self):
        if len(self.observations) < 2:
            return self

        # Maximum allowed gap in seconds
        MAX_GAP_SECONDS = 60

        timestamps = [obs.timestamp for obs in self.observations]

        for i in range(1, len(timestamps)):
            gap = (timestamps[i] - timestamps[i - 1]).total_seconds()
            if gap >= MAX_GAP_SECONDS:
                raise ValueError(
                    f"Temporal gap of {gap} seconds between observations at index "
                    f"{i-1} and {i} exceeds maximum allowed {MAX_GAP_SECONDS} seconds"
                )

        return self


