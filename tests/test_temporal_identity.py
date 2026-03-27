# --- Subsystem 8.1: Temporal Anchoring ---

import pytest
from datetime import datetime

# Core primitives
from tesla_core_protocol.primitives.observation import Observation
from tesla_core_protocol.primitives.stream import ObservationStream
from tesla_core_protocol.primitives.provenance import Provenance
from tesla_core_protocol.interpreter import DeterministicInterpreter


def test_temporal_anchor_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.1 — Temporal Anchoring

    A ReasoningTree must expose a deterministic temporal anchor derived solely
    from the root context timestamp. This anchor must remain stable across:

    - different interpreters
    - different branch_depth
    - different num_branches
    - different pruning settings
    - different internal structure

    This is the temporal analogue of the semantic nucleus.
    """

    # Fixed timestamp for deterministic anchoring
    fixed_ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_1_root",
        observations=[
            Observation(
                id="obs_8_1_root",
                timestamp=fixed_ts,
                source="user",
                content="temporal anchor root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="temporal anchor payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=None,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="temporal anchor payload",
        branch_depth=4,        # deeper
        num_branches=5,        # more branches
        prune_below_rank=2,    # pruning applied
    )

    sA = tree_a.summary
    sB = tree_b.summary

    # Both trees must expose a temporal anchor
    assert "temporal_anchor" in sA, "Tree A missing temporal anchor"
    assert "temporal_anchor" in sB, "Tree B missing temporal anchor"

    # Subsystem 8.1 invariant:
    # Temporal anchor must be identical across structurally different trees
    assert (
        sA["temporal_anchor"] == sB["temporal_anchor"]
    ), "Temporal anchor must be deterministic and structure-invariant (Subsystem 8.1)"

def test_temporal_continuity_hash_is_stable_and_timestamp_sensitive():
    """
    Subsystem 8.2 — Temporal Continuity Hash

    A ReasoningTree must expose a temporal continuity hash derived from:
    - the temporal anchor (root timestamp)
    - the unified identity hash
    - the root provenance hash

    This hash must be:
    - identical across structurally different trees with the same root timestamp
    - different when the root timestamp changes
    """

    from datetime import datetime

    # --- Case 1: identical timestamps → identical continuity hash ---
    fixed_ts = datetime(2020, 1, 1, 12, 0, 0)

    rootA = ObservationStream(
        id="stream_8_2_roota",
        observations=[
            Observation(
                id="obs_8_2_roota",
                timestamp=fixed_ts,
                source="user",
                content="temporal continuity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp1 = DeterministicInterpreter()
    treeA1 = interp1.reason_tree(
        context=rootA,
        content="temporal continuity payload",
        branch_depth=2,
        num_branches=3,
    )

    interp2 = DeterministicInterpreter()
    treeA2 = interp2.reason_tree(
        context=rootA,
        content="temporal continuity payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA1 = treeA1.summary
    sA2 = treeA2.summary

    assert "temporal_continuity_hash" in sA1
    assert "temporal_continuity_hash" in sA2

    # Must match for identical timestamps
    assert (
        sA1["temporal_continuity_hash"] == sA2["temporal_continuity_hash"]
    ), "Temporal continuity hash must be identical for identical timestamps"

    # --- Case 2: different timestamps → different continuity hash ---
    shifted_ts = datetime(2020, 1, 1, 12, 0, 1)  # +1 second

    rootB = ObservationStream(
        id="stream_8_2_rootb",
        observations=[
            Observation(
                id="obs_8_2_rootb",
                timestamp=shifted_ts,
                source="user",
                content="temporal continuity root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp3 = DeterministicInterpreter()
    treeB = interp3.reason_tree(
        context=rootB,
        content="temporal continuity payload",
        branch_depth=2,
        num_branches=3,
    )

    sB = treeB.summary

    # Must differ when timestamp differs
    assert (
        sA1["temporal_continuity_hash"] != sB["temporal_continuity_hash"]
    ), "Temporal continuity hash must differ when root timestamp differs"

def test_temporal_drift_field_is_present_and_defaults_to_none():
    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_3_root1",
        observations=[
            Observation(
                id="obs_8_3_root1",
                timestamp=ts,
                source="user",
                content="temporal drift root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="temporal drift payload",
        branch_depth=2,
        num_branches=3,
    )

    s = tree.summary

    assert "temporal_drift" in s
    assert s["temporal_drift"] == "none"

def test_temporal_stability_class_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.4 — Temporal Stability Class

    A ReasoningTree must expose a temporal stability class derived from the
    timestamp progression of the selected branch trace.

    Rules:
    - If all timestamp deltas are equal → "steady"
    - If deltas are strictly increasing → "advancing"
    - If deltas are strictly decreasing → "regressing"
    - Otherwise → "jumping"

    This classification must be deterministic and structure-invariant.
    """

    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_4_root",
        observations=[
            Observation(
                id="obs_8_4_root",
                timestamp=ts,
                source="user",
                content="temporal stability root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    treeA = interp1.reason_tree(
        context=root,
        content="temporal stability payload",
        branch_depth=2,
        num_branches=3,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    treeB = interp2.reason_tree(
        context=root,
        content="temporal stability payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA = treeA.summary
    sB = treeB.summary

    assert "temporal_stability_class" in sA
    assert "temporal_stability_class" in sB

    # Must match across structural differences
    assert (
        sA["temporal_stability_class"] == sB["temporal_stability_class"]
    ), "Temporal stability class must be structure-invariant"

def test_temporal_coherence_hash_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.5 — Temporal Coherence Hash

    A ReasoningTree must expose a unified temporal coherence hash derived from:
    - temporal_anchor
    - temporal_continuity_hash
    - temporal_drift
    - temporal_stability_class

    This hash must be:
    - deterministic
    - structure-invariant
    - timestamp-sensitive
    """

    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_5_root",
        observations=[
            Observation(
                id="obs_8_5_root",
                timestamp=ts,
                source="user",
                content="temporal coherence root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    treeA = interp1.reason_tree(
        context=root,
        content="temporal coherence payload",
        branch_depth=2,
        num_branches=3,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    treeB = interp2.reason_tree(
        context=root,
        content="temporal coherence payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA = treeA.summary
    sB = treeB.summary

    assert "temporal_coherence_hash" in sA
    assert "temporal_coherence_hash" in sB

    # Must match across structural differences
    assert (
        sA["temporal_coherence_hash"] == sB["temporal_coherence_hash"]
    ), "Temporal coherence hash must be structure-invariant"

    # --- Timestamp sensitivity check ---
    ts2 = datetime(2020, 1, 1, 12, 0, 1)  # +1 second

    root2 = ObservationStream(
        id="stream_8_5_root2",
        observations=[
            Observation(
                id="obs_8_5_root2",
                timestamp=ts2,
                source="user",
                content="temporal coherence root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp3 = DeterministicInterpreter()
    treeC = interp3.reason_tree(
        context=root2,
        content="temporal coherence payload",
        branch_depth=2,
        num_branches=3,
    )

    sC = treeC.summary

    assert (
        sA["temporal_coherence_hash"] != sC["temporal_coherence_hash"]
    ), "Temporal coherence hash must differ when timestamp differs"

def test_temporal_lineage_hash_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.6 — Temporal Lineage Surface

    A ReasoningTree must expose a temporal lineage hash derived from:
    - temporal_anchor
    - temporal_continuity_hash
    - temporal_stability_class

    This lineage hash must be:
    - deterministic
    - structure-invariant
    - timestamp-sensitive
    """

    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_6_root",
        observations=[
            Observation(
                id="obs_8_6_root",
                timestamp=ts,
                source="user",
                content="temporal lineage root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    treeA = interp1.reason_tree(
        context=root,
        content="temporal lineage payload",
        branch_depth=2,
        num_branches=3,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    treeB = interp2.reason_tree(
        context=root,
        content="temporal lineage payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA = treeA.summary
    sB = treeB.summary

    assert "temporal_lineage_hash" in sA
    assert "temporal_lineage_hash" in sB

    # Must match across structural differences
    assert (
        sA["temporal_lineage_hash"] == sB["temporal_lineage_hash"]
    ), "Temporal lineage hash must be structure-invariant"

    # --- Timestamp sensitivity check ---
    ts2 = datetime(2020, 1, 1, 12, 0, 1)  # +1 second

    root2 = ObservationStream(
        id="stream_8_6_root2",
        observations=[
            Observation(
                id="obs_8_6_root2",
                timestamp=ts2,
                source="user",
                content="temporal lineage root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp3 = DeterministicInterpreter()
    treeC = interp3.reason_tree(
        context=root2,
        content="temporal lineage payload",
        branch_depth=2,
        num_branches=3,
    )

    sC = treeC.summary

    assert (
        sA["temporal_lineage_hash"] != sC["temporal_lineage_hash"]
    ), "Temporal lineage hash must differ when timestamp differs"

def test_temporal_compression_hash_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.7 — Temporal Compression Surface

    A ReasoningTree must expose a temporal compression hash derived from the
    normalized timestamp deltas along the selected branch trace.

    This hash must be:
    - deterministic
    - structure-invariant
    - timestamp-sensitive
    """

    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_7_root",
        observations=[
            Observation(
                id="obs_8_7_root",
                timestamp=ts,
                source="user",
                content="temporal compression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    treeA = interp1.reason_tree(
        context=root,
        content="temporal compression payload",
        branch_depth=2,
        num_branches=3,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    treeB = interp2.reason_tree(
        context=root,
        content="temporal compression payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA = treeA.summary
    sB = treeB.summary

    assert "temporal_compression_hash" in sA
    assert "temporal_compression_hash" in sB

    # Must match across structural differences
    assert (
        sA["temporal_compression_hash"] == sB["temporal_compression_hash"]
    ), "Temporal compression hash must be structure-invariant"

    # --- Timestamp sensitivity check ---
    ts2 = datetime(2020, 1, 1, 12, 0, 1)  # +1 second

    root2 = ObservationStream(
        id="stream_8_7_root2",
        observations=[
            Observation(
                id="obs_8_7_root2",
                timestamp=ts2,
                source="user",
                content="temporal compression root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp3 = DeterministicInterpreter()
    treeC = interp3.reason_tree(
        context=root2,
        content="temporal compression payload",
        branch_depth=2,
        num_branches=3,
    )

    sC = treeC.summary

    assert (
        sA["temporal_compression_hash"] != sC["temporal_compression_hash"]
    ), "Temporal compression hash must differ when timestamp differs"

def test_temporal_provenance_hash_is_deterministic_and_structure_invariant():
    """
    Subsystem 8.8 — Temporal Provenance Weighting

    A ReasoningTree must expose a temporal provenance hash derived from:
    - temporal_anchor
    - temporal_continuity_hash
    - temporal_stability_class
    - root provenance confidence

    This hash must be:
    - deterministic
    - structure-invariant
    - timestamp-sensitive
    - provenance-sensitive
    """

    from datetime import datetime

    ts = datetime(2020, 1, 1, 12, 0, 0)

    root = ObservationStream(
        id="stream_8_8_root",
        observations=[
            Observation(
                id="obs_8_8_root",
                timestamp=ts,
                source="user",
                content="temporal provenance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.75,
                ),
            )
        ],
    )

    # Tree A — baseline
    interp1 = DeterministicInterpreter()
    treeA = interp1.reason_tree(
        context=root,
        content="temporal provenance payload",
        branch_depth=2,
        num_branches=3,
    )

    # Tree B — structurally different
    interp2 = DeterministicInterpreter()
    treeB = interp2.reason_tree(
        context=root,
        content="temporal provenance payload",
        branch_depth=4,
        num_branches=5,
        prune_below_rank=2,
    )

    sA = treeA.summary
    sB = treeB.summary

    assert "temporal_provenance_hash" in sA
    assert "temporal_provenance_hash" in sB

    # Must match across structural differences
    assert (
        sA["temporal_provenance_hash"] == sB["temporal_provenance_hash"]
    ), "Temporal provenance hash must be structure-invariant"

    # --- Timestamp sensitivity check ---
    ts2 = datetime(2020, 1, 1, 12, 0, 1)  # +1 second

    root2 = ObservationStream(
        id="stream_8_8_root2",
        observations=[
            Observation(
                id="obs_8_8_root2",
                timestamp=ts2,
                source="user",
                content="temporal provenance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.75,
                ),
            )
        ],
    )

    interp3 = DeterministicInterpreter()
    treeC = interp3.reason_tree(
        context=root2,
        content="temporal provenance payload",
        branch_depth=2,
        num_branches=3,
    )

    sC = treeC.summary

    assert (
        sA["temporal_provenance_hash"] != sC["temporal_provenance_hash"]
    ), "Temporal provenance hash must differ when timestamp differs"

    # --- Provenance sensitivity check ---
    root3 = ObservationStream(
        id="stream_8_8_root3",
        observations=[
            Observation(
                id="obs_8_8_root3",
                timestamp=ts,
                source="user",
                content="temporal provenance root",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.33,  # different confidence
                ),
            )
        ],
    )

    interp4 = DeterministicInterpreter()
    treeD = interp4.reason_tree(
        context=root3,
        content="temporal provenance payload",
        branch_depth=2,
        num_branches=3,
    )

    sD = treeD.summary

    assert (
        sA["temporal_provenance_hash"] != sD["temporal_provenance_hash"]
    ), "Temporal provenance hash must differ when provenance confidence differs"

