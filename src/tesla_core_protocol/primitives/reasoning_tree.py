# TESLA Core Protocol - Primitive: ReasoningTree
# Version: 0.1
# Status: Extracted from monolithic models.py (no behavior changes)
#
# ReasoningTree is a structural container for multi-branch reasoning.
# It does not enforce deep invariants yet — those will evolve in Subsystem 6.5+.
#
# This file is a pure extraction: no logic has been modified.

import hashlib
from typing import Dict, List, Tuple, Optional

from pydantic import BaseModel, ConfigDict, model_validator

from .stream import ObservationStream
from .observation import Observation
from .provenance import Provenance


class ReasoningTree(BaseModel):
    """
    A reasoning tree with:
    - a root context (ObservationStream)
    - a set of branches (each a stream or list of streams)
    - deterministic provenance
    - optional selection metadata
    """

    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
    )

    # Deterministic tree identity
    id: str

    # Core structure
    root_context: ObservationStream
    branches: Dict[str, ObservationStream | List[ObservationStream]]
    provenance: Provenance

    # Optional selection metadata
    selected_branch: Optional[str] = None
    selection_justification: Optional[dict] = None
    branch_scores: Optional[Dict[str, int]] = None
    branch_ranking: Optional[List[Tuple[str, int]]] = None
    selected_branch_trace: Optional[List[Observation]] = None
    branch_metadata: Optional[Dict[str, Dict]] = None
    summary: Optional[dict] = None

    @model_validator(mode="after")
    def assign_deterministic_id(self) -> "ReasoningTree":
        """
        Assign a deterministic tree id as a pure function of:
        - root_context.id
        - number of branches
        - sorted branch keys
        """
        identity_input = "|".join(
            [
                self.root_context.id,
                str(len(self.branches)),
                ",".join(sorted(self.branches.keys())),
            ]
        )

        deterministic_hash = hashlib.sha256(identity_input.encode("utf-8")).hexdigest()
        self.id = f"tree_{deterministic_hash[:16]}"
        return self


        
    