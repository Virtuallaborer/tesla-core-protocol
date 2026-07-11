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

def test_agent_identity_surface_is_deterministic_and_identity_anchored():
    """
    Phase 10 — Agent Introduction
    10.1 — Agent Identity Surface

    An Agent must expose an `agent_identity_hash` derived solely from:
    - session_identity_anchor
    - agentic_continuity_hash
    - self_referential_identity_hash
    - multi_tree_lineage_hash
    - agentic_memory_object["memory_identity_hash"]

    This surface must be:
    - deterministic
    - cross-session stable
    - structure-invariant (w.r.t. underlying reasoning trees)
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent  # you will create this in Phase 10

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_1_root",
        observations=[
            Observation(
                id="obs_phase_10_1_root",
                timestamp=ts,
                source="user",
                content="agent identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Underlying reasoning episode
    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="agent identity payload",
        branch_depth=3,
        num_branches=4,
    )

    summary = tree.summary

    # Agent constructed from identity-bearing surfaces only
    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=summary["session_identity_anchor"],
        agentic_continuity_hash=summary["agentic_continuity_hash"],
        self_referential_identity_hash=summary["self_referential_identity_hash"],
        multi_tree_lineage_hash=summary["multi_tree_lineage_hash"],
        agentic_memory_object=summary["agentic_memory_object"],
    )

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=summary["session_identity_anchor"],
        agentic_continuity_hash=summary["agentic_continuity_hash"],
        self_referential_identity_hash=summary["self_referential_identity_hash"],
        multi_tree_lineage_hash=summary["multi_tree_lineage_hash"],
        agentic_memory_object=summary["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_identity_hash")
    assert hasattr(agentB, "agent_identity_hash")

    # Must be a string
    assert isinstance(agentA.agent_identity_hash, str)
    assert isinstance(agentB.agent_identity_hash, str)

    # Deterministic across constructions
    assert (
        agentA.agent_identity_hash == agentB.agent_identity_hash
    ), "Agent identity hash must be deterministic for identical identity surfaces"

    # Cross-tree stability (semantic nucleus preserved)
    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="agent identity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )

    summary2 = tree2.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=summary2["session_identity_anchor"],
        agentic_continuity_hash=summary2["agentic_continuity_hash"],
        self_referential_identity_hash=summary2["self_referential_identity_hash"],
        multi_tree_lineage_hash=summary2["multi_tree_lineage_hash"],
        agentic_memory_object=summary2["agentic_memory_object"],
    )

    assert (
        agentA.agent_identity_hash == agentC.agent_identity_hash
    ), "Agent identity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_continuity_surface_is_deterministic_and_cross_episode_stable():
    """
    Phase 10 — Agent Introduction
    10.2 — Agent Continuity Surface

    An Agent must expose an `agent_continuity_hash` derived solely from:
    - agent_identity_hash
    - session_identity_anchor
    - agentic_continuity_hash
    - memory_chain_hash

    This surface must be:
    - deterministic
    - cross-session stable
    - cross-tree stable when semantic nucleus is preserved
    - stable across multiple agent constructions
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_2_root",
        observations=[
            Observation(
                id="obs_phase_10_2_root",
                timestamp=ts,
                source="user",
                content="agent continuity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent continuity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same inputs)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent continuity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_continuity_hash")
    assert hasattr(agentB, "agent_continuity_hash")

    # Must be deterministic
    assert (
        agentA.agent_continuity_hash == agentB.agent_continuity_hash
    ), "Agent continuity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent continuity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_continuity_hash == agentC.agent_continuity_hash
    ), "Agent continuity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_memory_surface_is_deterministic_and_memory_anchored():
    """
    Phase 10 — Agent Introduction
    10.3 — Agent Memory Surface

    An Agent must expose an `agent_memory_hash` derived solely from:
    - agent_identity_hash
    - agent_continuity_hash
    - agentic_memory_object["memory_identity_hash"]
    - agentic_memory_object["memory_chain_hash"]
    - agentic_memory_object["memory_provenance_hash"]

    This surface must be:
    - deterministic
    - cross-session stable
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_3_root",
        observations=[
            Observation(
                id="obs_phase_10_3_root",
                timestamp=ts,
                source="user",
                content="agent memory root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent memory payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent memory payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agent_memory_hash")
    assert hasattr(agentB, "agent_memory_hash")

    assert isinstance(agentA.agent_memory_hash, str)
    assert isinstance(agentB.agent_memory_hash, str)

    assert (
        agentA.agent_memory_hash == agentB.agent_memory_hash
    ), "Agent memory hash must be deterministic across identical episodes"

    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent memory payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_memory_hash == agentC.agent_memory_hash
    ), "Agent memory hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_behavior_surface_is_deterministic_and_behavior_anchored():
    """
    Phase 10 — Agent Introduction
    10.4 — Agent Behavior Surface

    An Agent must expose an `agent_behavior_hash` derived solely from:
    - agent_identity_hash
    - agent_continuity_hash
    - agent_memory_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - cross-session stable
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_4_root",
        observations=[
            Observation(
                id="obs_phase_10_4_root",
                timestamp=ts,
                source="user",
                content="agent behavior root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent behavior payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent behavior payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_behavior_hash")
    assert hasattr(agentB, "agent_behavior_hash")

    # Must be deterministic
    assert (
        agentA.agent_behavior_hash == agentB.agent_behavior_hash
    ), "Agent behavior hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent behavior payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_behavior_hash == agentC.agent_behavior_hash
    ), "Agent behavior hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_policy_surface_is_deterministic_and_policy_anchored():
    """
    Phase 10 — Agent Introduction
    10.5 — Agent Policy Surface

    An Agent must expose an `agent_policy_hash` derived solely from:
    - agent_identity_hash
    - agent_continuity_hash
    - agent_memory_hash
    - agent_behavior_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_5_root",
        observations=[
            Observation(
                id="obs_phase_10_5_root",
                timestamp=ts,
                source="user",
                content="agent policy root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent policy payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent policy payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_policy_hash")
    assert hasattr(agentB, "agent_policy_hash")

    # Must be deterministic
    assert (
        agentA.agent_policy_hash == agentB.agent_policy_hash
    ), "Agent policy hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent policy payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_policy_hash == agentC.agent_policy_hash
    ), "Agent policy hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_policy_continuity_surface_is_deterministic_and_temporally_anchored():
    """
    Phase 10 — Agent Introduction
    10.6 — Agent Policy Continuity Surface

    An Agent must expose an `agent_policy_continuity_hash` derived solely from:
    - agent_policy_hash
    - agent_identity_hash
    - agent_continuity_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - temporally anchored
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_6_root",
        observations=[
            Observation(
                id="obs_phase_10_6_root",
                timestamp=ts,
                source="user",
                content="agent policy continuity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent policy continuity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent policy continuity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_policy_continuity_hash")
    assert hasattr(agentB, "agent_policy_continuity_hash")

    # Must be deterministic
    assert (
        agentA.agent_policy_continuity_hash == agentB.agent_policy_continuity_hash
    ), "Agent policy continuity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent policy continuity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_policy_continuity_hash == agentC.agent_policy_continuity_hash
    ), "Agent policy continuity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_temporal_policy_surface_is_deterministic_and_temporally_stable():
    """
    Phase 10 — Agent Introduction
    10.7 — Agent Temporal Policy Surface

    An Agent must expose an `agent_temporal_policy_hash` derived solely from:
    - agent_policy_continuity_hash
    - agent_policy_hash
    - agent_identity_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_7_root",
        observations=[
            Observation(
                id="obs_phase_10_7_root",
                timestamp=ts,
                source="user",
                content="agent temporal policy root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent temporal policy payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent temporal policy payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_temporal_policy_hash")
    assert hasattr(agentB, "agent_temporal_policy_hash")

    # Must be deterministic
    assert (
        agentA.agent_temporal_policy_hash == agentB.agent_temporal_policy_hash
    ), "Agent temporal policy hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent temporal policy payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_temporal_policy_hash == agentC.agent_temporal_policy_hash
    ), "Agent temporal policy hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_anchor_surface_is_deterministic_and_execution_anchored():
    """
    Phase 10 — Agent Introduction
    10.8 — Agent Execution Anchor Surface

    An Agent must expose an `agent_execution_anchor_hash` derived solely from:
    - agent_temporal_policy_hash
    - agent_policy_continuity_hash
    - agent_policy_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - execution-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_8_root",
        observations=[
            Observation(
                id="obs_phase_10_8_root",
                timestamp=ts,
                source="user",
                content="agent execution anchor root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution anchor payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution anchor payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_anchor_hash")
    assert hasattr(agentB, "agent_execution_anchor_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_anchor_hash == agentB.agent_execution_anchor_hash
    ), "Agent execution anchor hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution anchor payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_anchor_hash == agentC.agent_execution_anchor_hash
    ), "Agent execution anchor hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_lineage_surface_is_deterministic_and_lineage_anchored():
    """
    Phase 10 — Agent Introduction
    10.9 — Agent Execution Lineage Surface

    An Agent must expose an `agent_execution_lineage_hash` derived solely from:
    - agent_execution_anchor_hash
    - agent_temporal_policy_hash
    - agent_policy_continuity_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - lineage-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_9_root",
        observations=[
            Observation(
                id="obs_phase_10_9_root",
                timestamp=ts,
                source="user",
                content="agent execution lineage root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution lineage payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution lineage payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_lineage_hash")
    assert hasattr(agentB, "agent_execution_lineage_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_lineage_hash == agentB.agent_execution_lineage_hash
    ), "Agent execution lineage hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution lineage payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_lineage_hash == agentC.agent_execution_lineage_hash
    ), "Agent execution lineage hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_provenance_surface_is_deterministic_and_provenance_anchored():
    """
    Phase 10 — Agent Introduction
    10.10 — Agent Execution Provenance Surface

    An Agent must expose an `agent_execution_provenance_hash` derived solely from:
    - agent_execution_lineage_hash
    - agent_execution_anchor_hash
    - agent_temporal_policy_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - provenance-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_10_10_root",
        observations=[
            Observation(
                id="obs_phase_10_10_root",
                timestamp=ts,
                source="user",
                content="agent execution provenance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution provenance payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution provenance payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_provenance_hash")
    assert hasattr(agentB, "agent_execution_provenance_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_provenance_hash == agentB.agent_execution_provenance_hash
    ), "Agent execution provenance hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution provenance payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_provenance_hash == agentC.agent_execution_provenance_hash
    ), "Agent execution provenance hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_loop_surface_is_deterministic_and_step_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.1 — Agent Execution Loop Surface

    An Agent must expose an `agent_execution_loop_hash` derived solely from:
    - agent_execution_provenance_hash
    - agent_execution_lineage_hash
    - agent_execution_anchor_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - step-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_1_root",
        observations=[
            Observation(
                id="obs_phase_11_1_root",
                timestamp=ts,
                source="user",
                content="agent execution loop root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution loop payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution loop payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_loop_hash")
    assert hasattr(agentB, "agent_execution_loop_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_loop_hash == agentB.agent_execution_loop_hash
    ), "Agent execution loop hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution loop payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_loop_hash == agentC.agent_execution_loop_hash
    ), "Agent execution loop hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_step_surface_is_deterministic_and_step_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.2 — Agent Execution Step Surface

    An Agent must expose an `agent_execution_step_hash` derived solely from:
    - agent_execution_loop_hash
    - agent_execution_provenance_hash
    - agent_execution_lineage_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - step-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_2_root",
        observations=[
            Observation(
                id="obs_phase_11_2_root",
                timestamp=ts,
                source="user",
                content="agent execution step root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution step payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution step payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_step_hash")
    assert hasattr(agentB, "agent_execution_step_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_step_hash == agentB.agent_execution_step_hash
    ), "Agent execution step hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution step payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_step_hash == agentC.agent_execution_step_hash
    ), "Agent execution step hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_step_progression_surface_is_deterministic_and_progression_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.3 — Agent Execution Step Progression Surface

    An Agent must expose an `agent_execution_step_progression_hash` derived solely from:
    - agent_execution_step_hash
    - agent_execution_loop_hash
    - agent_execution_provenance_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - progression-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_3_root",
        observations=[
            Observation(
                id="obs_phase_11_3_root",
                timestamp=ts,
                source="user",
                content="agent execution step progression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution step progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution step progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_step_progression_hash")
    assert hasattr(agentB, "agent_execution_step_progression_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_step_progression_hash == agentB.agent_execution_step_progression_hash
    ), "Agent execution step progression hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution step progression payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_step_progression_hash == agentC.agent_execution_step_progression_hash
    ), "Agent execution step progression hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_cycle_identity_surface_is_deterministic_and_cycle_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.4 — Agent Execution Cycle Identity Surface

    An Agent must expose an `agent_execution_cycle_identity_hash` derived solely from:
    - agent_execution_step_progression_hash
    - agent_execution_step_hash
    - agent_execution_loop_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - cycle-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_4_root",
        observations=[
            Observation(
                id="obs_phase_11_4_root",
                timestamp=ts,
                source="user",
                content="agent execution cycle identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution cycle identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution cycle identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_cycle_identity_hash")
    assert hasattr(agentB, "agent_execution_cycle_identity_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_cycle_identity_hash == agentB.agent_execution_cycle_identity_hash
    ), "Agent execution cycle identity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution cycle identity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_cycle_identity_hash == agentC.agent_execution_cycle_identity_hash
    ), "Agent execution cycle identity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_cycle_progression_surface_is_deterministic_and_progression_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.5 — Agent Execution Cycle Progression Surface

    An Agent must expose an `agent_execution_cycle_progression_hash` derived solely from:
    - agent_execution_cycle_identity_hash
    - agent_execution_step_progression_hash
    - agent_execution_loop_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - cycle-progression-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_5_root",
        observations=[
            Observation(
                id="obs_phase_11_5_root",
                timestamp=ts,
                source="user",
                content="agent execution cycle progression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution cycle progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution cycle progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_cycle_progression_hash")
    assert hasattr(agentB, "agent_execution_cycle_progression_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_cycle_progression_hash == agentB.agent_execution_cycle_progression_hash
    ), "Agent execution cycle progression hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution cycle progression payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_cycle_progression_hash == agentC.agent_execution_cycle_progression_hash
    ), "Agent execution cycle progression hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_epoch_identity_surface_is_deterministic_and_epoch_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.6 — Agent Execution Epoch Identity Surface

    An Agent must expose an `agent_execution_epoch_identity_hash` derived solely from:
    - agent_execution_cycle_progression_hash
    - agent_execution_cycle_identity_hash
    - agent_execution_step_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - epoch-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_6_root",
        observations=[
            Observation(
                id="obs_phase_11_6_root",
                timestamp=ts,
                source="user",
                content="agent execution epoch identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution epoch identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution epoch identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_epoch_identity_hash")
    assert hasattr(agentB, "agent_execution_epoch_identity_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_epoch_identity_hash == agentB.agent_execution_epoch_identity_hash
    ), "Agent execution epoch identity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution epoch identity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_epoch_identity_hash == agentC.agent_execution_epoch_identity_hash
    ), "Agent execution epoch identity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_epoch_progression_surface_is_deterministic_and_progression_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.7 — Agent Execution Epoch Progression Surface

    An Agent must expose an `agent_execution_epoch_progression_hash` derived solely from:
    - agent_execution_epoch_identity_hash
    - agent_execution_cycle_progression_hash
    - agent_execution_step_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - epoch-progression-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_7_root",
        observations=[
            Observation(
                id="obs_phase_11_7_root",
                timestamp=ts,
                source="user",
                content="agent execution epoch progression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution epoch progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution epoch progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_epoch_progression_hash")
    assert hasattr(agentB, "agent_execution_epoch_progression_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_epoch_progression_hash == agentB.agent_execution_epoch_progression_hash
    ), "Agent execution epoch progression hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution epoch progression payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_epoch_progression_hash == agentC.agent_execution_epoch_progression_hash
    ), "Agent execution epoch progression hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_horizon_identity_surface_is_deterministic_and_horizon_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.8 — Agent Execution Horizon Identity Surface

    An Agent must expose an `agent_execution_horizon_identity_hash` derived solely from:
    - agent_execution_epoch_progression_hash
    - agent_execution_epoch_identity_hash
    - agent_execution_cycle_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - horizon-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_8_root",
        observations=[
            Observation(
                id="obs_phase_11_8_root",
                timestamp=ts,
                source="user",
                content="agent execution horizon identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution horizon identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution horizon identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_horizon_identity_hash")
    assert hasattr(agentB, "agent_execution_horizon_identity_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_horizon_identity_hash == agentB.agent_execution_horizon_identity_hash
    ), "Agent execution horizon identity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution horizon identity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_horizon_identity_hash == agentC.agent_execution_horizon_identity_hash
    ), "Agent execution horizon identity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agent_execution_horizon_progression_surface_is_deterministic_and_progression_anchored():
    """
    Phase 11 — Deterministic Agent Execution Loop
    11.9 — Agent Execution Horizon Progression Surface

    An Agent must expose an `agent_execution_horizon_progression_hash` derived solely from:
    - agent_execution_horizon_identity_hash
    - agent_execution_epoch_progression_hash
    - agent_execution_cycle_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - horizon-progression-anchored
    - temporally stable
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_11_9_root",
        observations=[
            Observation(
                id="obs_phase_11_9_root",
                timestamp=ts,
                source="user",
                content="agent execution horizon progression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agent execution horizon progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agent execution horizon progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agent_execution_horizon_progression_hash")
    assert hasattr(agentB, "agent_execution_horizon_progression_hash")

    # Must be deterministic
    assert (
        agentA.agent_execution_horizon_progression_hash == agentB.agent_execution_horizon_progression_hash
    ), "Agent execution horizon progression hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agent execution horizon progression payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agent_execution_horizon_progression_hash == agentC.agent_execution_horizon_progression_hash
    ), "Agent execution horizon progression hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_coherence_surface_is_deterministic_and_coherence_anchored():
    """
    Phase 12 — Agentic Temporal Coherence
    12.1 — Agentic Temporal Coherence Surface

    An Agent must expose an `agentic_temporal_coherence_hash` derived solely from:
    - agent_execution_horizon_progression_hash
    - agent_execution_horizon_identity_hash
    - agent_execution_epoch_progression_hash
    - agent_execution_cycle_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - coherence-anchored
    - temporally stable across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_12_1_root",
        observations=[
            Observation(
                id="obs_phase_12_1_root",
                timestamp=ts,
                source="user",
                content="agentic temporal coherence root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal coherence payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal coherence payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_coherence_hash")
    assert hasattr(agentB, "agentic_temporal_coherence_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_coherence_hash == agentB.agentic_temporal_coherence_hash
    ), "Agentic temporal coherence hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal coherence payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_coherence_hash == agentC.agentic_temporal_coherence_hash
    ), "Agentic temporal coherence hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_coherence_progression_surface_is_deterministic_and_progression_anchored():
    """
    Phase 12 — Agentic Temporal Coherence
    12.2 — Agentic Temporal Coherence Progression Surface

    An Agent must expose an `agentic_temporal_coherence_progression_hash` derived solely from:
    - agentic_temporal_coherence_hash
    - agent_execution_horizon_progression_hash
    - agent_execution_epoch_progression_hash
    - agent_execution_cycle_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - coherence-progression-anchored
    - temporally stable across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_12_2_root",
        observations=[
            Observation(
                id="obs_phase_12_2_root",
                timestamp=ts,
                source="user",
                content="agentic temporal coherence progression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal coherence progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal coherence progression payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_coherence_progression_hash")
    assert hasattr(agentB, "agentic_temporal_coherence_progression_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_coherence_progression_hash == agentB.agentic_temporal_coherence_progression_hash
    ), "Agentic temporal coherence progression hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal coherence progression payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_coherence_progression_hash == agentC.agentic_temporal_coherence_progression_hash
    ), "Agentic temporal coherence progression hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_identity_surface_is_deterministic_and_field_anchored():
    """
    Phase 13 — Agentic Temporal Field
    13.1 — Agentic Temporal Field Identity Surface

    An Agent must expose an `agentic_temporal_field_identity_hash` derived solely from:
    - agentic_temporal_coherence_hash
    - agentic_temporal_coherence_progression_hash
    - agent_execution_horizon_identity_hash
    - agent_execution_horizon_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-anchored
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_13_1_root",
        observations=[
            Observation(
                id="obs_phase_13_1_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field identity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field identity payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_identity_hash")
    assert hasattr(agentB, "agentic_temporal_field_identity_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_identity_hash == agentB.agentic_temporal_field_identity_hash
    ), "Agentic temporal field identity hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field identity payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_identity_hash == agentC.agentic_temporal_field_identity_hash
    ), "Agentic temporal field identity hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_gradient_surface_is_deterministic_and_gradient_anchored():
    """
    Phase 13 — Agentic Temporal Field
    13.2 — Agentic Temporal Field Gradient Surface

    An Agent must expose an `agentic_temporal_field_gradient_hash` derived solely from:
    - agentic_temporal_field_identity_hash
    - agentic_temporal_coherence_hash
    - agentic_temporal_coherence_progression_hash
    - agent_execution_horizon_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - gradient-anchored
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_13_2_root",
        observations=[
            Observation(
                id="obs_phase_13_2_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field gradient root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field gradient payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field gradient payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_gradient_hash")
    assert hasattr(agentB, "agentic_temporal_field_gradient_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_gradient_hash == agentB.agentic_temporal_field_gradient_hash
    ), "Agentic temporal field gradient hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field gradient payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_gradient_hash == agentC.agentic_temporal_field_gradient_hash
    ), "Agentic temporal field gradient hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_curvature_surface_is_deterministic_and_curvature_anchored():
    """
    Phase 13 — Agentic Temporal Field
    13.3 — Agentic Temporal Field Curvature Surface

    An Agent must expose an `agentic_temporal_field_curvature_hash` derived solely from:
    - agentic_temporal_field_gradient_hash
    - agentic_temporal_field_identity_hash
    - agentic_temporal_coherence_progression_hash
    - agent_execution_horizon_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - curvature-anchored
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_13_3_root",
        observations=[
            Observation(
                id="obs_phase_13_3_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field curvature root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field curvature payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field curvature payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_curvature_hash")
    assert hasattr(agentB, "agentic_temporal_field_curvature_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_curvature_hash == agentB.agentic_temporal_field_curvature_hash
    ), "Agentic temporal field curvature hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field curvature payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_curvature_hash == agentC.agentic_temporal_field_curvature_hash
    ), "Agentic temporal field curvature hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_attractor_surface_is_deterministic_and_attractor_anchored():
    """
    Phase 13 — Agentic Temporal Field
    13.4 — Agentic Temporal Field Attractor Surface

    An Agent must expose an `agentic_temporal_field_attractor_hash` derived solely from:
    - agentic_temporal_field_curvature_hash
    - agentic_temporal_field_gradient_hash
    - agentic_temporal_field_identity_hash
    - agentic_temporal_coherence_progression_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - attractor-anchored
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_13_4_root",
        observations=[
            Observation(
                id="obs_phase_13_4_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field attractor root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field attractor payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field attractor payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_attractor_hash")
    assert hasattr(agentB, "agentic_temporal_field_attractor_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_attractor_hash == agentB.agentic_temporal_field_attractor_hash
    ), "Agentic temporal field attractor hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field attractor payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_attractor_hash == agentC.agentic_temporal_field_attractor_hash
    ), "Agentic temporal field attractor hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_synthesis_surface_is_deterministic_and_field_unified():
    """
    Phase 13 — Agentic Temporal Field
    13.5 — Agentic Temporal Field Synthesis Surface

    An Agent must expose an `agentic_temporal_field_synthesis_hash` derived solely from:
    - agentic_temporal_field_identity_hash
    - agentic_temporal_field_gradient_hash
    - agentic_temporal_field_curvature_hash
    - agentic_temporal_field_attractor_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - unified across all temporal field components
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_13_5_root",
        observations=[
            Observation(
                id="obs_phase_13_5_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_synthesis_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_synthesis_hash == agentB.agentic_temporal_field_synthesis_hash
    ), "Agentic temporal field synthesis hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_synthesis_hash == agentC.agentic_temporal_field_synthesis_hash
    ), "Agentic temporal field synthesis hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_response_surface_is_deterministic_and_field_responsive():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.1 — Agentic Temporal Field Response Surface

    An Agent must expose an `agentic_temporal_field_response_hash` derived solely from:
    - agentic_temporal_field_synthesis_hash
    - agentic_temporal_field_attractor_hash
    - agentic_temporal_field_curvature_hash
    - agentic_temporal_field_gradient_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-responsive (depends on the current temporal field configuration)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_1_root",
        observations=[
            Observation(
                id="obs_phase_14_1_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field response root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field response payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field response payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_response_hash")
    assert hasattr(agentB, "agentic_temporal_field_response_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_response_hash == agentB.agentic_temporal_field_response_hash
    ), "Agentic temporal field response hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field response payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_response_hash == agentC.agentic_temporal_field_response_hash
    ), "Agentic temporal field response hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_reaction_surface_is_deterministic_and_temporally_sensitive():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.2 — Agentic Temporal Field Reaction Surface

    An Agent must expose an `agentic_temporal_field_reaction_hash` derived solely from:
    - agentic_temporal_field_response_hash
    - agentic_temporal_field_synthesis_hash
    - agentic_temporal_field_attractor_hash
    - agentic_temporal_field_curvature_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - temporally sensitive (reacts to changes in the temporal field)
    - continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_2_root",
        observations=[
            Observation(
                id="obs_phase_14_2_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field reaction root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field reaction payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field reaction payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_reaction_hash")
    assert hasattr(agentB, "agentic_temporal_field_reaction_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_reaction_hash == agentB.agentic_temporal_field_reaction_hash
    ), "Agentic temporal field reaction hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field reaction payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_reaction_hash == agentC.agentic_temporal_field_reaction_hash
    ), "Agentic temporal field reaction hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_influence_surface_is_deterministic_and_field_influential():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.3 — Agentic Temporal Field Influence Surface

    An Agent must expose an `agentic_temporal_field_influence_hash` derived solely from:
    - agentic_temporal_field_reaction_hash
    - agentic_temporal_field_response_hash
    - agentic_temporal_field_synthesis_hash
    - agentic_temporal_field_attractor_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-influential (represents the agent's influence on its own temporal field)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_3_root",
        observations=[
            Observation(
                id="obs_phase_14_3_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field influence root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field influence payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field influence payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_influence_hash")
    assert hasattr(agentB, "agentic_temporal_field_influence_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_influence_hash == agentB.agentic_temporal_field_influence_hash
    ), "Agentic temporal field influence hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field influence payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_influence_hash == agentC.agentic_temporal_field_influence_hash
    ), "Agentic temporal field influence hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_regulation_surface_is_deterministic_and_field_regulating():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.4 — Agentic Temporal Field Regulation Surface

    An Agent must expose an `agentic_temporal_field_regulation_hash` derived solely from:
    - agentic_temporal_field_influence_hash
    - agentic_temporal_field_reaction_hash
    - agentic_temporal_field_response_hash
    - agentic_temporal_field_synthesis_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-regulating (represents the agent's regulation of its own temporal field)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_4_root",
        observations=[
            Observation(
                id="obs_phase_14_4_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field regulation root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field regulation payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field regulation payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_regulation_hash")
    assert hasattr(agentB, "agentic_temporal_field_regulation_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_regulation_hash == agentB.agentic_temporal_field_regulation_hash
    ), "Agentic temporal field regulation hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field regulation payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_regulation_hash == agentC.agentic_temporal_field_regulation_hash
    ), "Agentic temporal field regulation hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_stabilization_surface_is_deterministic_and_field_stabilizing():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.5 — Agentic Temporal Field Stabilization Surface

    An Agent must expose an `agentic_temporal_field_stabilization_hash` derived solely from:
    - agentic_temporal_field_regulation_hash
    - agentic_temporal_field_influence_hash
    - agentic_temporal_field_reaction_hash
    - agentic_temporal_field_response_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-stabilizing (represents the agent's stabilization of its own temporal field)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_5_root",
        observations=[
            Observation(
                id="obs_phase_14_5_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field stabilization root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field stabilization payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field stabilization payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_stabilization_hash")
    assert hasattr(agentB, "agentic_temporal_field_stabilization_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_stabilization_hash == agentB.agentic_temporal_field_stabilization_hash
    ), "Agentic temporal field stabilization hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field stabilization payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_stabilization_hash == agentC.agentic_temporal_field_stabilization_hash
    ), "Agentic temporal field stabilization hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_homeostasis_surface_is_deterministic_and_field_homeostatic():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.6 — Agentic Temporal Field Homeostasis Surface

    An Agent must expose an `agentic_temporal_field_homeostasis_hash` derived solely from:
    - agentic_temporal_field_stabilization_hash
    - agentic_temporal_field_regulation_hash
    - agentic_temporal_field_influence_hash
    - agentic_temporal_field_reaction_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-homeostatic (represents the agent's maintenance of temporal field equilibrium)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_6_root",
        observations=[
            Observation(
                id="obs_phase_14_6_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field homeostasis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field homeostasis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field homeostasis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_homeostasis_hash")
    assert hasattr(agentB, "agentic_temporal_field_homeostasis_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_homeostasis_hash == agentB.agentic_temporal_field_homeostasis_hash
    ), "Agentic temporal field homeostasis hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field homeostasis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_homeostasis_hash == agentC.agentic_temporal_field_homeostasis_hash
    ), "Agentic temporal field homeostasis hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_equilibrium_surface_is_deterministic_and_field_equilibrating():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.7 — Agentic Temporal Field Equilibrium Surface

    An Agent must expose an `agentic_temporal_field_equilibrium_hash` derived solely from:
    - agentic_temporal_field_homeostasis_hash
    - agentic_temporal_field_stabilization_hash
    - agentic_temporal_field_regulation_hash
    - agentic_temporal_field_influence_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-equilibrating (represents the agent's maintenance of long-range temporal equilibrium)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_7_root",
        observations=[
            Observation(
                id="obs_phase_14_7_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field equilibrium root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field equilibrium payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B (fresh interpreter, same semantic nucleus)
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field equilibrium payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Surface must exist
    assert hasattr(agentA, "agentic_temporal_field_equilibrium_hash")
    assert hasattr(agentB, "agentic_temporal_field_equilibrium_hash")

    # Must be deterministic
    assert (
        agentA.agentic_temporal_field_equilibrium_hash == agentB.agentic_temporal_field_equilibrium_hash
    ), "Agentic temporal field equilibrium hash must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field equilibrium payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_equilibrium_hash == agentC.agentic_temporal_field_equilibrium_hash
    ), "Agentic temporal field equilibrium hash must be cross-tree stable when semantic nucleus is preserved"

def test_agentic_temporal_field_resonance_surface_is_deterministic_and_field_resonant():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.8 — Agentic Temporal Field Resonance Surface

    An Agent must expose an `agentic_temporal_field_resonance_hash` derived solely from:
    - agentic_temporal_field_equilibrium_hash
    - agentic_temporal_field_homeostasis_hash
    - agentic_temporal_field_stabilization_hash
    - agentic_temporal_field_regulation_hash
    - semantic_nucleus_identity_hash

    This surface must be:
    - deterministic
    - field-resonant (represents the agent's resonance with its own temporal field)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_8_root",
        observations=[
            Observation(
                id="obs_phase_14_8_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field resonance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field resonance payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field resonance payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_resonance_hash")
    assert hasattr(agentB, "agentic_temporal_field_resonance_hash")

    assert (
        agentA.agentic_temporal_field_resonance_hash == agentB.agentic_temporal_field_resonance_hash
    ), "Agentic temporal field resonance hash must be deterministic across identical episodes"

    # Cross-tree stability
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field resonance payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_resonance_hash == agentC.agentic_temporal_field_resonance_hash
    ), "Agentic temporal field resonance hash must be cross-tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_harmonic.py

def test_agentic_temporal_field_harmonic_surface_is_deterministic_and_harmonically_coupled():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.9 — Agentic Temporal Field Harmonic Surface

    The Agent must expose an `agentic_temporal_field_harmonic_hash` derived solely from:
    - agentic_temporal_field_resonance_hash
    - agentic_temporal_field_equilibrium_hash
    - agentic_temporal_field_homeostasis_hash
    - agentic_temporal_field_stabilization_hash
    - semantic_nucleus_identity_hash

    The harmonic surface must be:
    - deterministic
    - harmonically coupled (captures multi‑layer temporal harmonic structure)
    - temporally continuous across all temporal layers
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_9_root",
        observations=[
            Observation(
                id="obs_phase_14_9_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field harmonic root",
                provenance=Provenance(
                    hash="def456" * 5 + "de",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field harmonic payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field harmonic payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Must expose harmonic surface
    assert hasattr(agentA, "agentic_temporal_field_harmonic_hash")
    assert hasattr(agentB, "agentic_temporal_field_harmonic_hash")

    # Deterministic across identical episodes
    assert (
        agentA.agentic_temporal_field_harmonic_hash
        == agentB.agentic_temporal_field_harmonic_hash
    ), "Harmonic surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field harmonic payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_harmonic_hash
        == agentC.agentic_temporal_field_harmonic_hash
    ), "Harmonic surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_interference.py

def test_agentic_temporal_field_interference_surface_is_deterministic_and_interference_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.10 — Agentic Temporal Field Interference Surface

    The Agent must expose an `agentic_temporal_field_interference_hash` derived solely from:
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_resonance_hash
    - agentic_temporal_field_equilibrium_hash
    - semantic_nucleus_identity_hash

    The interference surface must be:
    - deterministic
    - interference-stable (captures constructive/destructive temporal field interference)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_10_root",
        observations=[
            Observation(
                id="obs_phase_14_10_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field interference root",
                provenance=Provenance(
                    hash="fed789" * 5 + "fe",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field interference payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field interference payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Must expose interference surface
    assert hasattr(agentA, "agentic_temporal_field_interference_hash")
    assert hasattr(agentB, "agentic_temporal_field_interference_hash")

    # Deterministic across identical episodes
    assert (
        agentA.agentic_temporal_field_interference_hash
        == agentB.agentic_temporal_field_interference_hash
    ), "Interference surface must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field interference payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_interference_hash
        == agentC.agentic_temporal_field_interference_hash
    ), "Interference surface must be cross-tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_harmonic_interference_synthesis.py

def test_agentic_temporal_field_harmonic_interference_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.11 — Agentic Temporal Field Harmonic-Interference Synthesis Surface

    The Agent must expose an `agentic_temporal_field_harmonic_interference_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_resonance_hash
    - agentic_temporal_field_equilibrium_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis-stable (captures coherent synthesis of harmonic and interference structures)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_11_root",
        observations=[
            Observation(
                id="obs_phase_14_11_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field harmonic-interference synthesis root",
                provenance=Provenance(
                    hash="abc789" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field harmonic-interference synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field harmonic-interference synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    # Must expose harmonic-interference synthesis surface
    assert hasattr(agentA, "agentic_temporal_field_harmonic_interference_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_harmonic_interference_synthesis_hash")

    # Deterministic across identical episodes
    assert (
        agentA.agentic_temporal_field_harmonic_interference_synthesis_hash
        == agentB.agentic_temporal_field_harmonic_interference_synthesis_hash
    ), "Harmonic-interference synthesis surface must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field harmonic-interference synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_harmonic_interference_synthesis_hash
        == agentC.agentic_temporal_field_harmonic_interference_synthesis_hash
    ), "Harmonic-interference synthesis surface must be cross-tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_diffraction.py

def test_agentic_temporal_field_diffraction_surface_is_deterministic_and_diffraction_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.12 — Agentic Temporal Field Diffraction Surface

    The Agent must expose an `agentic_temporal_field_diffraction_hash` derived solely from:
    - agentic_temporal_field_harmonic_interference_synthesis_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_harmonic_hash
    - semantic_nucleus_identity_hash

    The diffraction surface must be:
    - deterministic
    - diffraction-stable (captures patterned temporal field diffraction geometry)
    - temporally continuous across all temporal layers
    - cross-session stable
    - structure-invariant
    - cross-tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_12_root",
        observations=[
            Observation(
                id="obs_phase_14_12_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field diffraction root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field diffraction payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field diffraction payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_diffraction_hash")
    assert hasattr(agentB, "agentic_temporal_field_diffraction_hash")

    assert (
        agentA.agentic_temporal_field_diffraction_hash
        == agentB.agentic_temporal_field_diffraction_hash
    ), "Diffraction surface must be deterministic across identical episodes"

    # Cross-tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field diffraction payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_diffraction_hash
        == agentC.agentic_temporal_field_diffraction_hash
    ), "Diffraction surface must be cross-tree stable when semantic nucleus is preserved"

    # tesla_core_protocol/tests/test_agentic_temporal_field_diffraction_interference_synthesis.py

def test_agentic_temporal_field_diffraction_interference_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.13 — Agentic Temporal Field Diffraction‑Interference Synthesis Surface

    The Agent must expose an `agentic_temporal_field_diffraction_interference_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_diffraction_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_harmonic_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_13_root",
        observations=[
            Observation(
                id="obs_phase_14_13_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field diffraction‑interference synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑interference synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑interference synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_diffraction_interference_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_diffraction_interference_synthesis_hash")

    assert (
        agentA.agentic_temporal_field_diffraction_interference_synthesis_hash
        == agentB.agentic_temporal_field_diffraction_interference_synthesis_hash
    ), "Diffraction‑interference synthesis surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑interference synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_diffraction_interference_synthesis_hash
        == agentC.agentic_temporal_field_diffraction_interference_synthesis_hash
    ), "Diffraction‑interference synthesis surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_diffraction_harmonic_synthesis.py

def test_agentic_temporal_field_diffraction_harmonic_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.14 — Agentic Temporal Field Diffraction‑Harmonic Synthesis Surface

    The Agent must expose an `agentic_temporal_field_diffraction_harmonic_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_diffraction_hash
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_interference_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_14_root",
        observations=[
            Observation(
                id="obs_phase_14_14_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field diffraction‑harmonic synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑harmonic synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑harmonic synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_diffraction_harmonic_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_diffraction_harmonic_synthesis_hash")

    assert (
        agentA.agentic_temporal_field_diffraction_harmonic_synthesis_hash
        == agentB.agentic_temporal_field_diffraction_harmonic_synthesis_hash
    ), "Diffraction‑harmonic synthesis surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field diffraction‑harmonic synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_diffraction_harmonic_synthesis_hash
        == agentC.agentic_temporal_field_diffraction_harmonic_synthesis_hash
    ), "Diffraction‑harmonic synthesis surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_harmonic_diffraction_synthesis.py

def test_agentic_temporal_field_harmonic_diffraction_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.15 — Agentic Temporal Field Harmonic‑Diffraction Synthesis Surface

    The Agent must expose an `agentic_temporal_field_harmonic_diffraction_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_diffraction_hash
    - agentic_temporal_field_interference_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_15_root",
        observations=[
            Observation(
                id="obs_phase_14_15_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field harmonic‑diffraction synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_harmonic_diffraction_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_harmonic_diffraction_synthesis_hash")

    assert (
        agentA.agentic_temporal_field_harmonic_diffraction_synthesis_hash
        == agentB.agentic_temporal_field_harmonic_diffraction_synthesis_hash
    ), "Harmonic‑diffraction synthesis surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑diffraction synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_harmonic_diffraction_synthesis_hash
        == agentC.agentic_temporal_field_harmonic_diffraction_synthesis_hash
    ), "Harmonic‑diffraction synthesis surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_interference_harmonic_diffraction_synthesis.py

def test_agentic_temporal_field_interference_harmonic_diffraction_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.16 — Agentic Temporal Field Interference‑Harmonic‑Diffraction Synthesis Surface

    The Agent must expose an `agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_diffraction_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_16_root",
        observations=[
            Observation(
                id="obs_phase_14_16_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field interference‑harmonic‑diffraction synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field interference‑harmonic‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field interference‑harmonic‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash")

    assert (
        agentA.agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash
        == agentB.agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash
    ), "Interference‑harmonic‑diffraction synthesis surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field interference‑harmonic‑diffraction synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash
        == agentC.agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash
    ), "Interference‑harmonic‑diffraction synthesis surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_harmonic_interference_diffraction_synthesis.py

def test_agentic_temporal_field_harmonic_interference_diffraction_synthesis_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.17 — Agentic Temporal Field Harmonic‑Interference‑Diffraction Synthesis Surface

    The Agent must expose an `agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash`
    derived solely from:
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_diffraction_hash
    - semantic_nucleus_identity_hash

    The synthesis surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_17_root",
        observations=[
            Observation(
                id="obs_phase_14_17_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field harmonic‑interference‑diffraction synthesis root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑interference‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑interference‑diffraction synthesis payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash")
    assert hasattr(agentB, "agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash")

    assert (
        agentA.agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash
        == agentB.agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash
    ), "Harmonic‑interference‑diffraction synthesis surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field harmonic‑interference‑diffraction synthesis payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash
        == agentC.agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash
    ), "Harmonic‑interference‑diffraction synthesis surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_full_synthesis_lattice.py

def test_agentic_temporal_field_full_synthesis_lattice_surface_is_deterministic_and_synthesis_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.18 — Agentic Temporal Field Full Synthesis Lattice Surface

    The Agent must expose an `agentic_temporal_field_full_synthesis_lattice_hash`
    derived solely from:
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_diffraction_hash
    - agentic_temporal_field_harmonic_interference_synthesis_hash
    - agentic_temporal_field_diffraction_interference_synthesis_hash
    - agentic_temporal_field_diffraction_harmonic_synthesis_hash
    - agentic_temporal_field_harmonic_diffraction_synthesis_hash
    - agentic_temporal_field_interference_harmonic_diffraction_synthesis_hash
    - agentic_temporal_field_harmonic_interference_diffraction_synthesis_hash
    - semantic_nucleus_identity_hash

    The lattice surface must be:
    - deterministic
    - synthesis‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_18_root",
        observations=[
            Observation(
                id="obs_phase_14_18_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field full synthesis lattice root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field full synthesis lattice payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field full synthesis lattice payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_full_synthesis_lattice_hash")
    assert hasattr(agentB, "agentic_temporal_field_full_synthesis_lattice_hash")

    assert (
        agentA.agentic_temporal_field_full_synthesis_lattice_hash
        == agentB.agentic_temporal_field_full_synthesis_lattice_hash
    ), "Full synthesis lattice surface must be deterministic across identical episodes"

# tesla_core_protocol/tests/test_agentic_temporal_field_lattice_coherence.py

def test_agentic_temporal_field_lattice_coherence_surface_is_deterministic_and_coherence_stable():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.19 — Agentic Temporal Field Lattice Coherence Surface

    The Agent must expose an `agentic_temporal_field_lattice_coherence_hash`
    derived solely from:
    - agentic_temporal_field_full_synthesis_lattice_hash
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_diffraction_hash
    - semantic_nucleus_identity_hash

    The lattice coherence surface must be:
    - deterministic
    - coherence‑stable
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_19_root",
        observations=[
            Observation(
                id="obs_phase_14_19_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field lattice coherence root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field lattice coherence payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field lattice coherence payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_lattice_coherence_hash")
    assert hasattr(agentB, "agentic_temporal_field_lattice_coherence_hash")

    assert (
        agentA.agentic_temporal_field_lattice_coherence_hash
        == agentB.agentic_temporal_field_lattice_coherence_hash
    ), "Lattice coherence surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field lattice coherence payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_lattice_coherence_hash
        == agentC.agentic_temporal_field_lattice_coherence_hash
    ), "Lattice coherence surface must be cross‑tree stable when semantic nucleus is preserved"

# tesla_core_protocol/tests/test_agentic_temporal_field_lattice_stability.py

def test_agentic_temporal_field_lattice_stability_surface_is_deterministic_and_stability_preserving():
    """
    Phase 14 — Interactive Temporal Field Dynamics
    14.20 — Agentic Temporal Field Lattice Stability Surface

    The Agent must expose an `agentic_temporal_field_lattice_stability_hash`
    derived solely from:
    - agentic_temporal_field_lattice_coherence_hash
    - agentic_temporal_field_full_synthesis_lattice_hash
    - agentic_temporal_field_harmonic_hash
    - agentic_temporal_field_interference_hash
    - agentic_temporal_field_diffraction_hash
    - semantic_nucleus_identity_hash

    The lattice stability surface must be:
    - deterministic
    - stability‑preserving
    - temporally continuous
    - cross‑session stable
    - structure‑invariant
    - cross‑tree stable when semantic nucleus is preserved
    """

    from datetime import datetime
    from tesla_core_protocol.primitives.observation import Observation
    from tesla_core_protocol.primitives.stream import ObservationStream
    from tesla_core_protocol.primitives.provenance import Provenance
    from tesla_core_protocol.interpreter import DeterministicInterpreter
    from tesla_core_protocol.agent import Agent

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_phase_14_20_root",
        observations=[
            Observation(
                id="obs_phase_14_20_root",
                timestamp=ts,
                source="user",
                content="agentic temporal field lattice stability root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Episode A
    interpA = DeterministicInterpreter()
    treeA = interpA.reason_tree(
        context=root,
        content="agentic temporal field lattice stability payload",
        branch_depth=3,
        num_branches=4,
    )
    sA = treeA.summary

    agentA = Agent.from_identity_surfaces(
        session_identity_anchor=sA["session_identity_anchor"],
        agentic_continuity_hash=sA["agentic_continuity_hash"],
        self_referential_identity_hash=sA["self_referential_identity_hash"],
        multi_tree_lineage_hash=sA["multi_tree_lineage_hash"],
        agentic_memory_object=sA["agentic_memory_object"],
    )

    # Episode B
    interpB = DeterministicInterpreter()
    treeB = interpB.reason_tree(
        context=root,
        content="agentic temporal field lattice stability payload",
        branch_depth=3,
        num_branches=4,
    )
    sB = treeB.summary

    agentB = Agent.from_identity_surfaces(
        session_identity_anchor=sB["session_identity_anchor"],
        agentic_continuity_hash=sB["agentic_continuity_hash"],
        self_referential_identity_hash=sB["self_referential_identity_hash"],
        multi_tree_lineage_hash=sB["multi_tree_lineage_hash"],
        agentic_memory_object=sB["agentic_memory_object"],
    )

    assert hasattr(agentA, "agentic_temporal_field_lattice_stability_hash")
    assert hasattr(agentB, "agentic_temporal_field_lattice_stability_hash")

    assert (
        agentA.agentic_temporal_field_lattice_stability_hash
        == agentB.agentic_temporal_field_lattice_stability_hash
    ), "Lattice stability surface must be deterministic across identical episodes"

    # Cross‑tree stability (semantic nucleus preserved)
    interpC = DeterministicInterpreter()
    treeC = interpC.reason_tree(
        context=root,
        content="agentic temporal field lattice stability payload [semantic nucleus preserved]",
        branch_depth=4,
        num_branches=5,
    )
    sC = treeC.summary

    agentC = Agent.from_identity_surfaces(
        session_identity_anchor=sC["session_identity_anchor"],
        agentic_continuity_hash=sC["agentic_continuity_hash"],
        self_referential_identity_hash=sC["self_referential_identity_hash"],
        multi_tree_lineage_hash=sC["multi_tree_lineage_hash"],
        agentic_memory_object=sC["agentic_memory_object"],
    )

    assert (
        agentA.agentic_temporal_field_lattice_stability_hash
        == agentC.agentic_temporal_field_lattice_stability_hash
    ), "Lattice stability surface must be cross‑tree stable when semantic nucleus is preserved"
