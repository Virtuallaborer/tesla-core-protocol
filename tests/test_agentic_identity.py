# ================================================================
#  Phase 9 — Emergent Agentic Behavior
#  Test File: test_agentic_identity.py
#
#  This file introduces the FIRST invariant of Phase 9:
#  Cross‑Session Identity Persistence.
#
#  Subsystem 6–8 established:
#    - deterministic reasoning substrate
#    - semantic–epistemic identity substrate
#    - temporal identity substrate
#
#  Phase 9 begins the transition from substrate → agent.
#  The first step is giving TESLA a stable identity across sessions.
# ================================================================

import pytest
from datetime import datetime

# ------------------------------------------------
#  Core TESLA Models
# ------------------------------------------------
from tesla_core_protocol.models import (
    Observation,
    ObservationStream,
    Provenance,
)

# ------------------------------------------------
#  Deterministic Interpreter
# ------------------------------------------------
from tesla_core_protocol.interpreter import DeterministicInterpreter


# ================================================================
#  9.1 — Cross‑Session Identity Persistence
#
#  A ReasoningTree must expose a `session_identity_anchor` derived
#  solely from the tri‑modal identity substrate:
#
#    - semantic_hash
#    - provenance_weighted_hash
#    - product_confidence
#    - temporal_coherence_hash
#
#  This anchor must be:
#    - deterministic
#    - structure‑invariant
#    - cross‑session stable
#
#  This is the FIRST AGENTIC INVARIANT.
#  It seeds the concept of "self" across sessions.
# ================================================================
def test_session_identity_anchor_is_deterministic_and_cross_session_stable():
    """
    Phase 9 — Emergent Agentic Behavior
    9.1 — Cross-Session Identity Persistence

    A ReasoningTree must expose a session_identity_anchor derived solely from:
    - semantic_hash
    - provenance_weighted_hash
    - product_confidence
    - temporal_coherence_hash

    This anchor must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    """

    # ------------------------------------------------
    #  Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_9_1_root",
        observations=[
            Observation(
                id="obs_9_1_root",
                timestamp=ts,
                source="user",
                content="agentic identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # ------------------------------------------------
    #  Session A — First Interpreter
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic identity payload",
        branch_depth=2,
        num_branches=3,
    )

    # ------------------------------------------------
    #  Session B — Fresh Interpreter, Same Inputs
    #  Must produce the SAME session_identity_anchor
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic identity payload",
        branch_depth=2,
        num_branches=3,
    )

    sA = treeA.summary
    sB = treeB.summary

    # ------------------------------------------------
    #  Invariant: Anchor must exist
    # ------------------------------------------------
    assert "session_identity_anchor" in sA
    assert "session_identity_anchor" in sB

    # ------------------------------------------------
    #  Invariant: Cross‑Session Stability
    # ------------------------------------------------
    assert (
        sA["session_identity_anchor"] == sB["session_identity_anchor"]
    ), "Session identity anchor must be cross-session stable"

    # ------------------------------------------------
    #  Structural Variation Test
    #  A structurally different tree must produce the SAME anchor
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic identity payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["session_identity_anchor"] == sC["session_identity_anchor"]
    ), "Session identity anchor must be structure-invariant"

def test_agentic_continuity_surface_is_deterministic_and_cross_session_stable():
    """
    Phase 9 — Emergent Agentic Behavior
    9.2 — Agentic Continuity Surface

    A ReasoningTree must expose an `agentic_continuity_hash` derived solely from:
    - session_identity_anchor        (Subsystem 9.1)
    - tree_identity_hash             (Subsystem 7.5)
    - temporal_continuity_hash       (Subsystem 8.2)

    This surface must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - sensitive only to identity-bearing surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    # ------------------------------------------------
    # Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_9_2_root",
        observations=[
            Observation(
                id="obs_9_2_root",
                timestamp=ts,
                source="user",
                content="agentic continuity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # ------------------------------------------------
    # Session A — First Interpreter
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic continuity payload",
        branch_depth=2,
        num_branches=3,
    )

    # ------------------------------------------------
    # Session B — Fresh Interpreter, Same Inputs
    # Must produce the SAME agentic_continuity_hash
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic continuity payload",
        branch_depth=2,
        num_branches=3,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Invariant: Surface must exist
    assert "agentic_continuity_hash" in sA
    assert "agentic_continuity_hash" in sB

    # Invariant: Cross-session stability
    assert (
        sA["agentic_continuity_hash"] == sB["agentic_continuity_hash"]
    ), "Agentic continuity hash must be cross-session stable"

    # ------------------------------------------------
    # Structural Variation Test
    # A structurally different tree must produce the SAME surface
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic continuity payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["agentic_continuity_hash"] == sC["agentic_continuity_hash"]
    ), "Agentic continuity hash must be structure-invariant"

def test_self_referential_identity_surface_is_deterministic_and_structure_invariant():
    """
    Phase 9 — Emergent Agentic Behavior
    9.3 — Self-Referential Reasoning

    A ReasoningTree must expose a `self_referential_identity_hash` derived solely from:
    - tree_identity_hash             (Subsystem 7.5)
    - session_identity_anchor        (Subsystem 9.1)
    - agentic_continuity_hash        (Subsystem 9.2)

    This surface must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - sensitive only to identity-bearing surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    # ------------------------------------------------
    # Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
    id="stream_phase_9_3_root",
    observations=[
        Observation(
            id="obs_phase_9_3_root",
            timestamp=ts,
            source="user",
            content="self referential root",
            provenance=Provenance(
                hash="abc123" * 5 + "ab",
                origin="user",
                confidence=0.9,
            ),
        )
    ],
)

    # ------------------------------------------------
    # Session A — First Interpreter
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="self referential payload",
        branch_depth=3,
        num_branches=4,
    )

    # ------------------------------------------------
    # Session B — Fresh Interpreter, Same Inputs
    # Must produce the SAME self_referential_identity_hash
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="self referential payload",
        branch_depth=3,
        num_branches=4,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "self_referential_identity_hash" in sA
    assert "self_referential_identity_hash" in sB

    # Cross-session stability
    assert (
        sA["self_referential_identity_hash"] == sB["self_referential_identity_hash"]
    ), "Self-referential identity hash must be cross-session stable"

    # ------------------------------------------------
    # Structural Variation Test
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="self referential payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["self_referential_identity_hash"] == sC["self_referential_identity_hash"]
    ), "Self-referential identity hash must be structure-invariant"

def test_multi_tree_lineage_hash_is_deterministic_and_cross_tree_stable():
    """
    Phase 9 — Emergent Agentic Behavior
    9.4 — Multi-Tree Lineage Graphs

    A ReasoningTree must expose a `multi_tree_lineage_hash` derived solely from:
    - self_referential_identity_hash   (Subsystem 9.3)
    - agentic_continuity_hash          (Subsystem 9.2)
    - session_identity_anchor          (Subsystem 9.1)

    This surface must be:
    - deterministic
    - cross-session stable
    - structure-invariant
    - cross-tree stable
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    # ------------------------------------------------
    # Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_9_4_root",
        observations=[
            Observation(
                id="obs_phase_9_4_root",
                timestamp=ts,
                source="user",
                content="multi tree lineage root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # ------------------------------------------------
    # Tree A — First reasoning episode
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="lineage payload",
        branch_depth=2,
        num_branches=3,
    )

    # ------------------------------------------------
    # Tree B — Second reasoning episode, same inputs
    # Must produce SAME lineage hash
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="lineage payload",
        branch_depth=2,
        num_branches=3,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "multi_tree_lineage_hash" in sA
    assert "multi_tree_lineage_hash" in sB

    # Cross-session stability
    assert (
        sA["multi_tree_lineage_hash"] == sB["multi_tree_lineage_hash"]
    ), "Lineage hash must be cross-session stable"

    # ------------------------------------------------
    # Structural Variation Test
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="lineage payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["multi_tree_lineage_hash"] == sC["multi_tree_lineage_hash"]
    ), "Lineage hash must be structure-invariant"

    # ------------------------------------------------
    # Cross-tree stability test
    # Tree D uses different content but same semantic nucleus
    # ------------------------------------------------
    interpD = DeterministicInterpreter()
    treeD = interpD.reason_tree(
        context=root,
        content="lineage payload [extra noise]",
        branch_depth=3,
        num_branches=4,
    )

    sD = treeD.summary

    assert (
        sA["multi_tree_lineage_hash"] == sD["multi_tree_lineage_hash"]
    ), "Lineage hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_memory_object_is_deterministic_and_identity_anchored():
    """
    Phase 9 — Emergent Agentic Behavior
    9.5 — Agentic Memory Substrate

    A ReasoningTree must expose an `agentic_memory_object` derived solely from:
    - session_identity_anchor        (Subsystem 9.1)
    - agentic_continuity_hash        (Subsystem 9.2)
    - self_referential_identity_hash (Subsystem 9.3)
    - multi_tree_lineage_hash        (Subsystem 9.4)

    This object must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - sensitive only to identity-bearing surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    # ------------------------------------------------
    # Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_9_5_root",
        observations=[
            Observation(
                id="obs_phase_9_5_root",
                timestamp=ts,
                source="user",
                content="agentic memory root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # ------------------------------------------------
    # Session A — First reasoning episode
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic memory payload",
        branch_depth=3,
        num_branches=4,
    )

    # ------------------------------------------------
    # Session B — Fresh interpreter, same inputs
    # Must produce SAME memory object
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic memory payload",
        branch_depth=3,
        num_branches=4,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "agentic_memory_object" in sA
    assert "agentic_memory_object" in sB

    # Must be a dict-like object
    assert isinstance(sA["agentic_memory_object"], dict)
    assert isinstance(sB["agentic_memory_object"], dict)

    # Cross-session stability
    assert (
        sA["agentic_memory_object"] == sB["agentic_memory_object"]
    ), "Agentic memory object must be cross-session stable"

    # ------------------------------------------------
    # Structural Variation Test
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic memory payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["agentic_memory_object"] == sC["agentic_memory_object"]
    ), "Agentic memory object must be structure-invariant"

    # ------------------------------------------------
    # Cross-tree stability test
    # ------------------------------------------------
    interpD = DeterministicInterpreter()
    treeD = interpD.reason_tree(
        context=root,
        content="agentic memory payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )

    sD = treeD.summary

    assert (
        sA["agentic_memory_object"] == sD["agentic_memory_object"]
    ), "Agentic memory object must be cross-tree stable when semantic nucleus is preserved"

def test_memory_stability_class_is_deterministic_and_identity_anchored():
    """
    Phase 9 — Emergent Agentic Behavior
    9.6 — Memory Stability Class

    A ReasoningTree must expose a `memory_stability_class` derived solely from:
    - session_identity_anchor
    - agentic_continuity_hash
    - self_referential_identity_hash
    - multi_tree_lineage_hash
    - agentic_memory_object["memory_identity_hash"]

    This class must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - cross-tree stable
    - sensitive only to identity-bearing surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    # ------------------------------------------------
    # Root Observation Setup
    # ------------------------------------------------
    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_9_6_root",
        observations=[
            Observation(
                id="obs_phase_9_6_root",
                timestamp=ts,
                source="user",
                content="memory stability root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # ------------------------------------------------
    # Tree A — First reasoning episode
    # ------------------------------------------------
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="memory stability payload",
        branch_depth=3,
        num_branches=4,
    )

    # ------------------------------------------------
    # Tree B — Fresh interpreter, same inputs
    # Must produce SAME stability class
    # ------------------------------------------------
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="memory stability payload",
        branch_depth=3,
        num_branches=4,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "memory_stability_class" in sA
    assert "memory_stability_class" in sB

    # Must be a string
    assert isinstance(sA["memory_stability_class"], str)
    assert isinstance(sB["memory_stability_class"], str)

    # Cross-session stability
    assert (
        sA["memory_stability_class"] == sB["memory_stability_class"]
    ), "Memory stability class must be cross-session stable"

    # ------------------------------------------------
    # Structural Variation Test
    # ------------------------------------------------
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="memory stability payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["memory_stability_class"] == sC["memory_stability_class"]
    ), "Memory stability class must be structure-invariant"

    # ------------------------------------------------
    # Cross-tree stability test
    # ------------------------------------------------
    interpD = DeterministicInterpreter()
    treeD = interpD.reason_tree(
        context=root,
        content="memory stability payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )

    sD = treeD.summary

    assert (
        sA["memory_stability_class"] == sD["memory_stability_class"]
    ), "Memory stability class must be cross-tree stable when semantic nucleus is preserved"

def test_memory_chain_surface_is_deterministic_and_identity_anchored():
    """
    Phase 9 — Emergent Agentic Behavior
    9.7 — Memory Chain Surface

    A ReasoningTree must expose a `memory_chain_hash` derived solely from:
    - agentic_memory_object["memory_identity_hash"]
    - memory_stability_class
    - multi_tree_lineage_hash

    This surface must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - cross-tree stable
    - sensitive only to identity-bearing surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_9_7_root",
        observations=[
            Observation(
                id="obs_phase_9_7_root",
                timestamp=ts,
                source="user",
                content="memory chain root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="memory chain payload",
        branch_depth=3,
        num_branches=4,
    )

    # Tree B (fresh interpreter, same inputs)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="memory chain payload",
        branch_depth=3,
        num_branches=4,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "memory_chain_hash" in sA
    assert "memory_chain_hash" in sB

    # Must be deterministic across sessions
    assert (
        sA["memory_chain_hash"] == sB["memory_chain_hash"]
    ), "Memory chain hash must be cross-session stable"

    # Structural variation
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="memory chain payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["memory_chain_hash"] == sC["memory_chain_hash"]
    ), "Memory chain hash must be structure-invariant"

    # Cross-tree stability (semantic nucleus preserved)
    interpD = DeterministicInterpreter()
    treeD = interpD.reason_tree(
        context=root,
        content="memory chain payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )

    sD = treeD.summary

    assert (
        sA["memory_chain_hash"] == sD["memory_chain_hash"]
    ), "Memory chain hash must be cross-tree stable"

def test_memory_provenance_surface_is_deterministic_and_provenance_anchored():
    """
    Phase 9 — Emergent Agentic Behavior
    9.8 — Memory Provenance Surface

    A ReasoningTree must expose a `memory_provenance_hash` derived solely from:
    - agentic_memory_object["memory_identity_hash"]
    - memory_stability_class
    - memory_chain_hash
    - temporal_provenance_hash

    This surface must be:
    - deterministic
    - structure-invariant
    - cross-session stable
    - cross-tree stable
    - sensitive only to identity-bearing and temporal-provenance surfaces
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_9_8_root",
        observations=[
            Observation(
                id="obs_phase_9_8_root",
                timestamp=ts,
                source="user",
                content="memory provenance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="memory provenance payload",
        branch_depth=3,
        num_branches=4,
    )

    # Tree B (fresh interpreter, same inputs)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="memory provenance payload",
        branch_depth=3,
        num_branches=4,
    )

    sA = treeA.summary
    sB = treeB.summary

    # Surface must exist
    assert "memory_provenance_hash" in sA
    assert "memory_provenance_hash" in sB

    # Must be a string
    assert isinstance(sA["memory_provenance_hash"], str)
    assert isinstance(sB["memory_provenance_hash"], str)

    # Cross-session stability
    assert (
        sA["memory_provenance_hash"] == sB["memory_provenance_hash"]
    ), "Memory provenance hash must be cross-session stable"

    # Structural variation
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="memory provenance payload",
        branch_depth=5,
        num_branches=6,
        prune_below_rank=2,
    )

    sC = treeC.summary

    assert (
        sA["memory_provenance_hash"] == sC["memory_provenance_hash"]
    ), "Memory provenance hash must be structure-invariant"

    # Cross-tree stability (semantic nucleus preserved)
    interpD = DeterministicInterpreter()
    treeD = interpD.reason_tree(
        context=root,
        content="memory provenance payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )

    sD = treeD.summary

    assert (
        sA["memory_provenance_hash"] == sD["memory_provenance_hash"]
    ), "Memory provenance hash must be cross-tree stable"
