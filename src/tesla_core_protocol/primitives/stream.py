# TESLA Core Protocol - Primitive: ObservationStream
# Status: Extracted from monolithic models.py (no behavior changes)

from datetime import timedelta
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, PrivateAttr, Field, model_validator, field_validator

from .observation import Observation


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
        if not self.observations:
            return self

        timestamps = [obs.timestamp for obs in self.observations]

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
        if len(self.observations) < 2:
            return self

        for prev, curr in zip(self.observations, self.observations[1:]):
            if prev.source == "tool" and curr.source == "environment":
                raise ValueError("Invalid source transition: tool → environment")

            if prev.source == "memory" and curr.source == "environment":
                raise ValueError("Invalid source transition: memory → environment")

            if prev.source == "memory" and curr.source == "tool":
                raise ValueError("Invalid source transition: memory → tool")

            if prev.source == "tool" and curr.source == "user":
                raise ValueError("Invalid source transition: tool → user")

            if prev.source == "memory" and curr.source == "user":
                raise ValueError("Invalid source transition: memory → user")

            if prev.source == "user" and curr.source == "system":
                raise ValueError("Invalid source transition: user → system")

            if prev.source == "environment" and curr.source == "system":
                raise ValueError("Invalid source transition: environment → system")

            if prev.source == "tool" and curr.source == "system":
                raise ValueError("Invalid source transition: tool → system")

            if prev.source == "memory" and curr.source == "system":
                raise ValueError("Invalid source transition: memory → system")

            if prev.source == "system" and curr.source == "memory":
                raise ValueError("Invalid source transition: system → memory")

            if prev.source == "tool" and curr.source == "memory":
                raise ValueError("Invalid source transition: tool → memory")

            if prev.source == "user" and curr.source == "tool":
                raise ValueError("Invalid source transition: user → tool")

            if prev.source == "environment" and curr.source == "memory":
                raise ValueError("Invalid source transition: environment → memory")

            if prev.source == "system" and curr.source == "user":
                raise ValueError("Invalid source transition: system → user")

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
