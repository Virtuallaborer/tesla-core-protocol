from datetime import datetime

from tesla_core_protocol.interpreter import DeterministicInterpreter
from tesla_core_protocol.primitives.stream import ObservationStream
from tesla_core_protocol.primitives.observation import Observation
from tesla_core_protocol.primitives.provenance import Provenance



def test_reasoning_tree_branches_share_root_context_id():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_000001",
        observations=[
            Observation(
                id="obs_root_000001",
                timestamp=fixed_ts,
                source="user",
                content="hello",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=1,
        num_branches=2,
    )

    # Assert: every branch shares the same root_context.id
    assert tree.root_context.id == root.id
    for key, branch in tree.branches.items():
        if isinstance(branch, list):
            for step in branch:
                assert tree.root_context.id == root.id
        else:
            assert tree.root_context.id == root.id

def test_reasoning_tree_branch_timestamps_not_before_root():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_000002",
        observations=[
            Observation(
                id="obs_root_000002",
                timestamp=fixed_ts,
                source="user",
                content="hello",
                provenance=Provenance(
                    hash="b" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=2,
        num_branches=3,
    )

    root_ts = root.observations[-1].timestamp

    # Assert: every branch’s timestamps must be >= root timestamp
    for key, branch in tree.branches.items():
        if isinstance(branch, list):
            # internal steps exposed
            for step_stream in branch:
                for obs in step_stream.observations:
                    assert obs.timestamp >= root_ts
        else:
            # single final stream
            for obs in branch.observations:
                assert obs.timestamp >= root_ts

def test_reasoning_tree_branch_provenance_origin_matches_tree():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_000003",
        observations=[
            Observation(
                id="obs_root_000003",
                timestamp=fixed_ts,
                source="user",
                content="hello",
                provenance=Provenance(
                    hash="c" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=2,
        num_branches=3,
    )

    tree_origin = tree.provenance.origin

    # Assert: every branch’s final observation must share the tree's provenance origin
    for key, branch in tree.branches.items():
        if isinstance(branch, list):
            final_obs = branch[-1].observations[-1]
        else:
            final_obs = branch.observations[-1]

        assert final_obs.provenance.origin == tree_origin

def test_reasoning_tree_selected_branch_trace_contains_final_observation():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_000004",
        observations=[
            Observation(
                id="obs_root_000004",
                timestamp=fixed_ts,
                source="user",
                content="hello",
                provenance=Provenance(
                    hash="d" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=3,
        num_branches=3,
    )

    selected_key = tree.selected_branch
    selected_branch = tree.branches[selected_key]

    # Get the final observation of the selected branch
    if isinstance(selected_branch, list):
        final_obs = selected_branch[-1].observations[-1]
    else:
        final_obs = selected_branch.observations[-1]

    # Assert: the final observation must appear in selected_branch_trace
    trace_ids = [obs.id for obs in tree.selected_branch_trace]
    assert final_obs.id in trace_ids

def test_reasoning_tree_id_is_deterministic():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_000010",
        observations=[
            Observation(
                id="obs_root_000010",
                timestamp=fixed_ts,
                source="user",
                content="hello",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree_1 = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=2,
        num_branches=3,
    )

    tree_2 = interp.reason_tree(
        context=root,
        content="world",
        branch_depth=2,
        num_branches=3,
    )

    # Both trees must expose a deterministic id
    assert hasattr(tree_1, "id")
    assert hasattr(tree_2, "id")

    # And that id must be identical for identical inputs
    assert tree_1.id == tree_2.id

def test_reasoning_tree_structural_equivalence_for_identical_inputs():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_struct_0001",
        observations=[
            Observation(
                id="obs_root_struct_0001",
                timestamp=fixed_ts,
                source="user",
                content="seed",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp_1 = DeterministicInterpreter()
    interp_2 = DeterministicInterpreter()

    tree_1 = interp_1.reason_tree(
        context=root,
        content="branching",
        branch_depth=2,
        num_branches=3,
    )

    # Clear registries again so the second interpreter can reuse IDs deterministically
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    tree_2 = interp_2.reason_tree(
        context=root,
        content="branching",
        branch_depth=2,
        num_branches=3,
    )

    # Structural equivalence: full model dump must match
    assert tree_1.model_dump() == tree_2.model_dump()

def test_reasoning_tree_rejects_semantically_contradictory_branch():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_semantic_0001",
        observations=[
            Observation(
                id="obs_root_semantic_0001",
                timestamp=fixed_ts,
                source="user",
                content="The sky is blue.",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="The sky is not blue.",
        branch_depth=1,
        num_branches=2,
    )

    # 6.6.C invariant: no branch may semantically contradict the root context.
    # For now, we encode a simple monotonicity rule:
    # the selected branch's final content must not be a direct negation.
    selected_key = tree.selected_branch
    assert selected_key is not None

    selected_branch = tree.branches[selected_key]
    if isinstance(selected_branch, list):
        final_obs = selected_branch[-1].observations[0]
    else:
        final_obs = selected_branch.observations[0]

    assert "not blue" not in final_obs.content

def test_reasoning_tree_branches_share_semantic_nucleus():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_semantic_nucleus_0001",
        observations=[
            Observation(
                id="obs_root_semantic_nucleus_0001",
                timestamp=fixed_ts,
                source="user",
                content="The sky is blue.",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    # Intentionally give content that could drift semantically
    tree = interp.reason_tree(
        context=root,
        content="Birds migrate south.",
        branch_depth=1,
        num_branches=3,
    )

    # 6.6.D invariant: all branches must share a semantic nucleus with the root.
    root_keywords = set(root.observations[-1].content.lower().split())

    for key, branch in tree.branches.items():
        if isinstance(branch, list):
            final_obs = branch[-1].observations[0]
        else:
            final_obs = branch.observations[0]

        branch_keywords = set(final_obs.content.lower().split())

        # Must share at least one keyword with the root
        assert len(root_keywords.intersection(branch_keywords)) > 0

def test_reasoning_tree_selected_branch_trace_matches_branch():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_trace_0001",
        observations=[
            Observation(
                id="obs_root_trace_0001",
                timestamp=fixed_ts,
                source="user",
                content="trace test",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="branching",
        branch_depth=2,
        num_branches=3,
    )

    selected = tree.selected_branch
    assert selected is not None

    branch = tree.branches[selected]

    # Extract actual sequence of observations from the selected branch
    if isinstance(branch, list):
        actual_trace = [obs for stream in branch for obs in stream.observations]
    else:
        actual_trace = branch.observations

    # selected_branch_trace must match exactly
    assert tree.selected_branch_trace is not None
    assert [obs.id for obs in tree.selected_branch_trace] == [obs.id for obs in actual_trace]

def test_reasoning_tree_provenance_reflects_semantic_divergence_between_branches():
    # Reset registries to avoid cross-test collisions
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0001",
        observations=[
            Observation(
                id="obs_root_6_7_0001",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
    )

    b1 = tree.branches["branch_0001"]
    b2 = tree.branches["branch_0002"]

    if isinstance(b1, list):
        final_1 = b1[-1].observations[0]
        final_2 = b2[-1].observations[0]
    else:
        final_1 = b1.observations[0]
        final_2 = b2.observations[0]

    # 6.7 invariant (Option 3):
    # Semantic divergence between branches must be reflected in provenance.
    # First, branches must be semantically distinct:
    assert final_1.content != final_2.content

    # Then, their final provenance hashes must differ:
    assert final_1.provenance.hash != final_2.provenance.hash

import hashlib

def test_reasoning_tree_tree_provenance_anchors_selected_branch_semantics():
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0002",
        observations=[
            Observation(
                id="obs_root_6_7_0002",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="b" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()

    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
    )

    concatenated_content = "".join(
        obs.content for obs in tree.selected_branch_trace
    ).encode("utf-8")

    semantic_hash = hashlib.sha256(concatenated_content).hexdigest()

    # 6.7.1 invariant:
    # The summary's tree_provenance_hash must be a semantic hash
    # of the selected reasoning path.
    assert semantic_hash == tree.summary["tree_provenance_hash"]

import hashlib

def test_reasoning_tree_semantic_provenance_stable_across_identical_trees():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0003",
        observations=[
            Observation(
                id="obs_root_6_7_0003",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="c" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # First interpreter / tree
    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Second interpreter / tree
    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
    )

    # Selected-branch semantics must match
    contents_1 = [obs.content for obs in tree1.selected_branch_trace]
    contents_2 = [obs.content for obs in tree2.selected_branch_trace]
    assert contents_1 == contents_2

    # Semantic provenance must match
    assert tree1.summary["tree_provenance_hash"] == tree2.summary["tree_provenance_hash"]

def test_reasoning_tree_semantic_equivalence_implies_semantic_surface_equivalence():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0004",
        observations=[
            Observation(
                id="obs_root_6_7_0004",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="d" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — no pruning
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=None,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — pruned to top 1 branch
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=1,
    )

    # Both trees must have identical semantic hashes
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.7.3 invariant:
    # Semantic equivalence implies semantic-surface equivalence.
    # The selected branch must be the same.
    assert tree_a.selected_branch == tree_b.selected_branch

    # The selected branch trace contents must be identical.
    contents_a = [obs.content for obs in tree_a.selected_branch_trace]
    contents_b = [obs.content for obs in tree_b.selected_branch_trace]
    assert contents_a == contents_b

    # The selection justification must match on semantic grounds.
    assert tree_a.selection_justification["selected_branch"] == tree_b.selection_justification["selected_branch"]
    assert tree_a.selection_justification["selected_branch_final_hash"] == tree_b.selection_justification["selected_branch_final_hash"]

def test_reasoning_tree_semantic_equivalence_implies_provenance_confidence_equivalence():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0005",
        observations=[
            Observation(
                id="obs_root_6_7_0005",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="e" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches, all retained
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches, all retained
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence: same selected-branch semantics → same semantic hash
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.7.4 invariant:
    # With semantic equivalence, adding more branches must not increase confidence.
    assert tree_a.provenance.confidence <= tree_b.provenance.confidence

def test_reasoning_tree_semantic_equivalence_implies_selected_branch_provenance_equivalence():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0006",
        observations=[
            Observation(
                id="obs_root_6_7_0006",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="f" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence: same selected-branch semantics → same semantic hash
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # Extract final observation of selected branch for both trees
    def final_obs(tree):
        branch = tree.branches[tree.selected_branch]
        if isinstance(branch, list):
            return branch[-1].observations[0]
        return branch.observations[0]

    final_a = final_obs(tree_a)
    final_b = final_obs(tree_b)

    # 6.7.5 invariant:
    # Semantic equivalence across trees implies equivalence of the selected branch's provenance hash.
    assert final_a.provenance.hash == final_b.provenance.hash

def test_reasoning_tree_semantic_equivalence_implies_semantic_id_equivalence():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_7_0007",
        observations=[
            Observation(
                id="obs_root_6_7_0007",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="f" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence: same semantic hash
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.7.6 invariant:
    # Semantically equivalent trees must expose a semantic identity field that is identical.
    assert tree_a.summary.get("semantic_id") == tree_b.summary.get("semantic_id")

def test_reasoning_tree_semantic_equivalence_implies_semantic_summary_equivalence():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_8_0001",
        observations=[
            Observation(
                id="obs_root_6_8_0001",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence: same semantic hash
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.8.0 invariant:
    # Semantically equivalent trees must expose a stable semantic_summary.
    assert "semantic_summary" in tree_a.summary
    assert "semantic_summary" in tree_b.summary
    assert tree_a.summary["semantic_summary"] == tree_b.summary["semantic_summary"]

def test_reasoning_tree_semantic_summary_includes_normalized_tokens():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_8_0002",
        observations=[
            Observation(
                id="obs_root_6_8_0002",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="b" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # 6.8.1 invariant:
    # semantic_summary must include a normalized token list.
    assert "semantic_summary" in tree.summary
    summary = tree.summary["semantic_summary"]

    # Must contain a token list
    assert "tokens" in summary
    assert isinstance(summary["tokens"], list)

    # Tokens must be lowercase, alphanumeric-only
    for tok in summary["tokens"]:
        assert tok == tok.lower()
        assert tok.isalnum()

def test_reasoning_tree_semantic_summary_includes_token_frequencies():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_8_0003",
        observations=[
            Observation(
                id="obs_root_6_8_0003",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="c" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # semantic_summary must exist
    assert "semantic_summary" in tree.summary
    summary = tree.summary["semantic_summary"]

    # Must contain tokens
    assert "tokens" in summary
    tokens = summary["tokens"]
    assert isinstance(tokens, list)

    # 6.8.2 invariant:
    # semantic_summary must include token frequencies
    assert "token_frequencies" in summary
    freqs = summary["token_frequencies"]
    assert isinstance(freqs, dict)

    # Frequencies must match actual token counts
    from collections import Counter
    expected = Counter(tokens)
    assert freqs == dict(expected)

def test_reasoning_tree_semantic_summary_includes_stable_fingerprint():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_8_0004",
        observations=[
            Observation(
                id="obs_root_6_8_0004",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="d" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # semantic_summary must exist
    assert "semantic_summary" in tree.summary
    summary = tree.summary["semantic_summary"]

    # Must contain tokens and frequencies
    assert "tokens" in summary
    assert "token_frequencies" in summary

    # 6.8.3 invariant:
    # semantic_summary must include a stable fingerprint
    assert "fingerprint" in summary
    fp = summary["fingerprint"]
    assert isinstance(fp, str)

    # Fingerprint must be deterministic:
    # sorted tokens expanded by frequency, joined with '-'
    from collections import Counter
    expected_tokens = summary["tokens"]
    expected_freqs = summary["token_frequencies"]

    # Reconstruct expected fingerprint
    expanded = []
    for tok, count in expected_freqs.items():
        expanded.extend([tok] * count)
    expected = "-".join(sorted(expanded))

    assert fp == expected

def test_reasoning_tree_semantic_summary_stable_across_semantically_equivalent_trees():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_8_0005",
        observations=[
            Observation(
                id="obs_root_6_8_0005",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="e" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence: same semantic hash
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.8.4 invariant:
    # Entire semantic_summary must be identical
    assert tree_a.summary["semantic_summary"] == tree_b.summary["semantic_summary"]

def test_reasoning_tree_semantic_summary_includes_provenance_weighted_tokens():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_9_0001",
        observations=[
            Observation(
                id="obs_root_6_9_0001",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="f" * 32,
                    origin="user",
                    confidence=1.0,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    assert "semantic_summary" in tree.summary
    summary = tree.summary["semantic_summary"]

    # 6.9.0 invariant:
    # semantic_summary must include provenance-weighted token scores
    assert "provenance_weighted_tokens" in summary
    pwt = summary["provenance_weighted_tokens"]
    assert isinstance(pwt, dict)

    # Scores must be floats
    for tok, score in pwt.items():
        assert isinstance(tok, str)
        assert isinstance(score, float)
        assert score > 0.0

def test_reasoning_tree_semantic_summary_includes_provenance_weighted_fingerprint():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_9_0002",
        observations=[
            Observation(
                id="obs_root_6_9_0002",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="a" * 32,
                    origin="user",
                    confidence=0.8,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    summary = tree.summary["semantic_summary"]

    # Must contain provenance-weighted tokens
    assert "provenance_weighted_tokens" in summary

    # 6.9.1 invariant:
    # semantic_summary must include a provenance-weighted fingerprint
    assert "provenance_fingerprint" in summary
    pf = summary["provenance_fingerprint"]
    assert isinstance(pf, str)

    # Provenance fingerprint must sort tokens by descending weight, then lexicographically
    pwt = summary["provenance_weighted_tokens"]
    expected = "-".join(
        tok for tok, _ in sorted(
            pwt.items(),
            key=lambda kv: (-kv[1], kv[0])
        )
    )

    assert pf == expected

def test_reasoning_tree_includes_provenance_weighted_semantic_hash():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_9_0003",
        observations=[
            Observation(
                id="obs_root_6_9_0003",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="b" * 32,
                    origin="user",
                    confidence=0.5,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    summary = tree.summary["semantic_summary"]

    # Must contain provenance-weighted tokens
    assert "provenance_weighted_tokens" in summary

    # 6.9.2 invariant:
    # semantic_summary must include a provenance-weighted semantic hash
    assert "provenance_weighted_hash" in summary
    pwh = summary["provenance_weighted_hash"]
    assert isinstance(pwh, str)

    # Hash must be deterministic:
    # sorted list of "token:score" pairs, joined, then hashed with sha256
    import hashlib

    pwt = summary["provenance_weighted_tokens"]
    items = [f"{tok}:{pwt[tok]}" for tok in sorted(pwt.keys())]
    joined = "|".join(items)
    expected_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()

    assert pwh == expected_hash

def test_reasoning_tree_provenance_weighted_hash_stable_across_semantically_equivalent_trees():
    # Reset registries before first tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_9_0004",
        observations=[
            Observation(
                id="obs_root_6_9_0004",
                timestamp=fixed_ts,
                source="user",
                content="root semantic anchor",
                provenance=Provenance(
                    hash="c" * 32,
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Tree A — 3 branches
    interp1 = DeterministicInterpreter()
    tree_a = interp1.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Tree B — 2 branches
    interp2 = DeterministicInterpreter()
    tree_b = interp2.reason_tree(
        context=root,
        content="branch semantic payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Semantic equivalence
    assert tree_a.summary["tree_provenance_hash"] == tree_b.summary["tree_provenance_hash"]

    # 6.9.3 invariant:
    # provenance-weighted hash must also be identical
    a_hash = tree_a.summary["semantic_summary"]["provenance_weighted_hash"]
    b_hash = tree_b.summary["semantic_summary"]["provenance_weighted_hash"]

    assert a_hash == b_hash

def test_reasoning_tree_includes_confidence_summary_for_selected_branch():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_10_0001",
        observations=[
            Observation(
                id="obs_root_6_10_0001",
                timestamp=fixed_ts,
                source="user",
                content="root epistemic anchor",
                provenance=Provenance(
                    hash="d" * 32,
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch epistemic payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    summary = tree.summary

    # 6.10.0 invariant:
    # summary must include a confidence_summary for the selected branch trace
    assert "confidence_summary" in summary
    cs = summary["confidence_summary"]
    assert isinstance(cs, dict)

    for key in ["min_confidence", "max_confidence", "product_confidence"]:
        assert key in cs
        assert isinstance(cs[key], float)

    # Product confidence must match the product of confidences along the selected branch trace
    product = 1.0
    for obs in tree.selected_branch_trace:
        product *= obs.provenance.confidence

    assert cs["product_confidence"] == product

def test_reasoning_tree_includes_confidence_gradient():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_10_0002",
        observations=[
            Observation(
                id="obs_root_6_10_0002",
                timestamp=fixed_ts,
                source="user",
                content="root epistemic anchor",
                provenance=Provenance(
                    hash="e" * 32,
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch epistemic payload",
        branch_depth=3,
        num_branches=3,
        prune_below_rank=3,
    )

    summary = tree.summary
    assert "confidence_summary" in summary

    cs = summary["confidence_summary"]
    assert "confidence_gradient" in cs
    gradient = cs["confidence_gradient"]

    assert isinstance(gradient, list)
    assert all(isinstance(x, float) for x in gradient)

    # Gradient length must be len(trace) - 1
    trace_conf = [obs.provenance.confidence for obs in tree.selected_branch_trace]
    assert len(gradient) == max(0, len(trace_conf) - 1)

    # Gradient must match pairwise differences
    expected = [
        float(trace_conf[i+1] - trace_conf[i])
        for i in range(len(trace_conf) - 1)
    ]
    assert gradient == expected

def test_reasoning_tree_includes_confidence_stability_class():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_10_0003",
        observations=[
            Observation(
                id="obs_root_6_10_0003",
                timestamp=fixed_ts,
                source="user",
                content="root epistemic anchor",
                provenance=Provenance(
                    hash="f" * 32,
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp = DeterministicInterpreter()
    tree = interp.reason_tree(
        context=root,
        content="branch epistemic payload",
        branch_depth=3,
        num_branches=3,
        prune_below_rank=3,
    )

    cs = tree.summary["confidence_summary"]
    assert "stability_class" in cs
    sc = cs["stability_class"]
    assert isinstance(sc, str)

    # Stability class must be one of the canonical categories
    allowed = {"increasing", "decreasing", "flat", "oscillating"}
    assert sc in allowed

    # Validate classification logic
    gradient = cs["confidence_gradient"]

    if not gradient:
        assert sc == "flat"
    elif all(g > 0 for g in gradient):
        assert sc == "increasing"

    elif all(g < 0 for g in gradient):
        assert sc == "decreasing"
    elif all(g == 0 for g in gradient):
        assert sc == "flat"
    else:
        assert sc == "oscillating"

def test_reasoning_tree_includes_unified_identity_hash_and_is_stable():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_6_11_0001",
        observations=[
            Observation(
                id="obs_root_6_11_0001",
                timestamp=fixed_ts,
                source="user",
                content="root identity anchor",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="identity payload",
        branch_depth=3,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries before second run
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="identity payload",
        branch_depth=3,
        num_branches=3,
        prune_below_rank=3,
    )

    s1 = tree1.summary
    s2 = tree2.summary

    assert "tree_identity_hash" in s1
    assert isinstance(s1["tree_identity_hash"], str)

    assert s1["tree_identity_hash"] == s2["tree_identity_hash"]

def test_cross_tree_identity_convergence_for_semantically_equivalent_trees():
    # Reset registries to avoid ID collisions across runs
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_7_5_0001",
        observations=[
            Observation(
                id="obs_root_7_5_0001",
                timestamp=fixed_ts,
                source="user",
                content="cross-tree identity anchor",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # First tree: shallower, fewer branches
    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="semantically equivalent identity payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Reset registries to force structurally different IDs in the second tree
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Second tree: deeper, more branches (different structure),
    # but same semantic nucleus in the input payload.
    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="semantically equivalent identity payload",
        branch_depth=3,
        num_branches=3,
        prune_below_rank=3,
    )

    s1 = tree1.summary
    s2 = tree2.summary

    # Both trees should expose a unified identity hash
    assert "tree_identity_hash" in s1
    assert "tree_identity_hash" in s2
    assert isinstance(s1["tree_identity_hash"], str)
    assert isinstance(s2["tree_identity_hash"], str)

    # Subsystem 7.5 invariant:
    # Semantically equivalent trees (same nucleus, different structure)
    # must converge to the same unified identity hash.
    assert (
        s1["tree_identity_hash"] == s2["tree_identity_hash"]
    ), "Semantically equivalent trees must converge to the same unified identity hash under Subsystem 7.5"

def test_identity_preserving_transformations_do_not_change_unified_identity_hash():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_7_6_0001",
        observations=[
            Observation(
                id="obs_root_7_6_0001",
                timestamp=fixed_ts,
                source="user",
                content="identity transform anchor",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Base tree
    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="identity transform payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    # Reset registries to force structural differences
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Transformed tree: add an extra inference step BEFORE reasoning
    # This transformation does NOT change the semantic nucleus.
    interp2 = DeterministicInterpreter()
    extra_step = interp2.infer(
        context=root,
        content="identity transform payload"
    )

    tree2 = interp2.reason_tree(
        context=extra_step,
        content="identity transform payload",
        branch_depth=2,
        num_branches=2,
        prune_below_rank=2,
    )

    s1 = tree1.summary
    s2 = tree2.summary

    # Both trees must expose identity hashes
    assert "tree_identity_hash" in s1
    assert "tree_identity_hash" in s2

    # Subsystem 7.6 invariant:
    # Identity-preserving transformations must not change the unified identity hash.
    assert (
        s1["tree_identity_hash"] == s2["tree_identity_hash"]
    ), "Identity-preserving transformations must not alter the unified identity hash under Subsystem 7.6"

def test_identity_stable_under_pruning_when_selected_branch_semantics_unchanged():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_7_7_0001",
        observations=[
            Observation(
                id="obs_root_7_7_0001",
                timestamp=fixed_ts,
                source="user",
                content="identity pruning anchor",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Base tree: no pruning
    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="identity pruning payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=None,
    )

    # Reset registries to force structural differences
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Pruned tree: prune to top 2 branches.
    # As long as the selected branch remains the same and its semantic nucleus
    # is unchanged, identity must remain stable.
    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="identity pruning payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=2,
    )

    s1 = tree1.summary
    s2 = tree2.summary

    # Sanity: both expose identity hashes and selected branches
    assert "tree_identity_hash" in s1
    assert "tree_identity_hash" in s2
    assert "selected_branch" in s1
    assert "selected_branch" in s2

    # 7.7 precondition: selected branch must be the same
    assert s1["selected_branch"] == s2["selected_branch"]

    # 7.7 invariant:
    # Pruning that preserves the selected branch's semantic nucleus
    # must not change the unified identity hash.
    assert (
        s1["tree_identity_hash"] == s2["tree_identity_hash"]
    ), "Identity must remain stable under pruning when the selected branch semantics are unchanged (Subsystem 7.7)"

def test_identity_stable_under_branch_count_changes_when_selected_branch_semantics_unchanged():
    # Reset registries
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    from datetime import datetime
    fixed_ts = datetime(2020, 1, 1, 0, 0, 0)

    root = ObservationStream(
        id="stream_root_7_8_0001",
        observations=[
            Observation(
                id="obs_root_7_8_0001",
                timestamp=fixed_ts,
                source="user",
                content="identity branchcount anchor",
                provenance=Provenance(
                    hash="abc123" * 5 + "ab",
                    origin="user",
                    confidence=0.9,
                ),
            )
        ],
    )

    # Base tree: 3 branches
    interp1 = DeterministicInterpreter()
    tree1 = interp1.reason_tree(
        context=root,
        content="identity branchcount payload",
        branch_depth=2,
        num_branches=3,
        prune_below_rank=3,
    )

    # Reset registries to force structural differences
    Observation._used_ids.clear()  # type: ignore[attr-defined]
    ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

    # Expanded tree: 7 branches
    interp2 = DeterministicInterpreter()
    tree2 = interp2.reason_tree(
        context=root,
        content="identity branchcount payload",
        branch_depth=2,
        num_branches=7,
        prune_below_rank=7,
    )

    s1 = tree1.summary
    s2 = tree2.summary

    # Both trees must expose identity hashes and selected branches
    assert "tree_identity_hash" in s1
    assert "tree_identity_hash" in s2
    assert "selected_branch" in s1
    assert "selected_branch" in s2

    # 7.8 precondition: selected branch must be the same
    assert s1["selected_branch"] == s2["selected_branch"]

    # 7.8 invariant:
    # Changing the number of non-selected branches must not change identity
    # when the selected branch semantics are unchanged.
    assert (
        s1["tree_identity_hash"] == s2["tree_identity_hash"]
    ), "Identity must remain stable under branch count changes when selected branch semantics are unchanged (Subsystem 7.8)"


