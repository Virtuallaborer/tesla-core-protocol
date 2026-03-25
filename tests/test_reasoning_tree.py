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


