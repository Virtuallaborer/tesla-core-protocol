import pytest
import hashlib

from datetime import datetime, timedelta
from pydantic import ValidationError

from tesla_core_protocol.models import Observation, ObservationStream

from tesla_core_protocol import DeterministicInterpreter
from tesla_core_protocol.models import ReasoningTree

@pytest.fixture(autouse=True)
def reset_registries():
    Observation._used_ids.clear()
    ObservationStream._used_stream_ids.clear()

@pytest.fixture(autouse=True)
def reset_observation_registry():
    Observation._used_ids.clear()


def test_interpreter_emits_system_scoped_thought_stream():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    # Build a simple user stream as input context
    obs1 = Observation(**{
        "id": "obs_ctx_001",
        "timestamp": ts,
        "source": "user",
        "content": "User says hello",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_ctx_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "User asks a question",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_001",
        "observations": [obs1, obs2],
    })

    interpreter = DeterministicInterpreter()

    thought_stream = interpreter.infer(
        context=ctx_stream,
        content="Interpreter derives a logical consequence.",
    )

    # Must be a new ObservationStream
    assert isinstance(thought_stream, ObservationStream)
    assert thought_stream.id != ctx_stream.id
    assert len(thought_stream.observations) == 1

    thought = thought_stream.observations[0]

    # 6.1.1: system-scoped thought
    assert thought.source == "system"
    assert thought.provenance.origin == "system"

    # Timestamp must not regress relative to context
    assert thought.timestamp >= ctx_stream.observations[-1].timestamp

def test_interpreter_ids_are_namespaced_and_monotonic():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_ids_001",
        "timestamp": ts,
        "source": "user",
        "content": "Context event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_ids_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out1 = interpreter.infer(context=ctx_stream, content="First thought")
    out2 = interpreter.infer(context=ctx_stream, content="Second thought")

    # Both outputs must be valid streams with a single observation
    assert isinstance(out1, ObservationStream)
    assert isinstance(out2, ObservationStream)
    assert len(out1.observations) == 1
    assert len(out2.observations) == 1

    obs1 = out1.observations[0]
    obs2 = out2.observations[0]

    # Namespacing
    assert obs1.id.startswith("obs_sys_")
    assert obs2.id.startswith("obs_sys_")
    assert out1.id.startswith("stream_sys_")
    assert out2.id.startswith("stream_sys_")

    # Monotonicity across calls on the same interpreter instance
    assert obs1.id < obs2.id
    assert out1.id < out2.id

def test_interpreter_timestamps_are_monotonic_and_deterministic():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_ts_001",
        "timestamp": ts,
        "source": "user",
        "content": "Context event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_ts_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out1 = interpreter.infer(context=ctx_stream, content="First")
    out2 = interpreter.infer(context=ctx_stream, content="Second")

    t1 = out1.observations[0].timestamp
    t2 = out2.observations[0].timestamp

    # Must be strictly increasing
    assert t1 > ts
    assert t2 > t1

    # Must be deterministic relative to call order
    # (no randomness, no system clock)
    assert (t2 - t1).total_seconds() < 60

def test_interpreter_provenance_hash_is_deterministic_and_monotonic():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_hash_001",
        "timestamp": ts,
        "source": "user",
        "content": "Context event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_hash_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out1 = interpreter.infer(context=ctx_stream, content="First logical step")
    out2 = interpreter.infer(context=ctx_stream, content="Second logical step")

    h1 = out1.observations[0].provenance.hash
    h2 = out2.observations[0].provenance.hash

    # Must be lowercase hex
    assert all(c in "0123456789abcdef" for c in h1)
    assert all(c in "0123456789abcdef" for c in h2)

    # Must be deterministic length (SHA-256 = 64 chars)
    assert len(h1) == 64
    assert len(h2) == 64

    # Must be strictly non-decreasing lexicographically
    assert h1 <= h2

    # Must be deterministic relative to inputs
    # (same interpreter, same context, same content → same hash)
    out1_again = interpreter.infer(context=ctx_stream, content="First logical step")
    h1_again = out1_again.observations[0].provenance.hash
    assert h1_again >= h1  # monotonicity is the invariant

def test_interpreter_content_is_deterministically_derived():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_content_001",
        "timestamp": ts,
        "source": "user",
        "content": "User states a fact.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_content_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out = interpreter.infer(context=ctx_stream, content="Interpreter processes this.")

    derived = out.observations[0].content

    # Must follow deterministic derivation rule
    assert derived == "Derived: User states a fact. -> Interpreter processes this."

def test_interpreter_confidence_is_deterministic():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_conf_001",
        "timestamp": ts,
        "source": "user",
        "content": "User provides context.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_conf_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out1 = interpreter.infer(context=ctx_stream, content="First inference.")
    out2 = interpreter.infer(context=ctx_stream, content="Second inference.")

    c1 = out1.observations[0].provenance.confidence
    c2 = out2.observations[0].provenance.confidence

    # Must follow deterministic rule: 1 / (1 + counter)
    assert c1 == 1 / 2
    assert c2 == 1 / 3

    # Must be strictly decreasing
    assert c2 < c1

def test_interpreter_multi_step_inference_is_deterministic_and_coherent():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_chain_001",
        "timestamp": ts,
        "source": "user",
        "content": "User provides initial context.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_chain_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    out1 = interpreter.infer(context=ctx_stream, content="First step.")
    out2 = interpreter.infer(context=ctx_stream, content="Second step.")
    out3 = interpreter.infer(context=ctx_stream, content="Third step.")

    o1 = out1.observations[0]
    o2 = out2.observations[0]
    o3 = out3.observations[0]

    # IDs must be strictly increasing
    assert o1.id < o2.id < o3.id

    # Timestamps must be strictly increasing
    assert o1.timestamp < o2.timestamp < o3.timestamp

    # Provenance hashes must be non-decreasing
    h1 = o1.provenance.hash
    h2 = o2.provenance.hash
    h3 = o3.provenance.hash
    assert h1 <= h2 <= h3

    # Confidence must follow 1 / (1 + counter)
    assert o1.provenance.confidence == 1 / 2
    assert o2.provenance.confidence == 1 / 3
    assert o3.provenance.confidence == 1 / 4

    # Content must remain deterministically derived
    assert o1.content == "Derived: User provides initial context. -> First step."
    assert o2.content == "Derived: User provides initial context. -> Second step."
    assert o3.content == "Derived: User provides initial context. -> Third step."

def test_interpreter_can_chain_its_own_outputs():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    # Initial user context
    obs = Observation(**{
        "id": "obs_ctx_chain2_001",
        "timestamp": ts,
        "source": "user",
        "content": "User begins the chain.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_chain2_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # First system inference
    out1 = interpreter.infer(context=ctx_stream, content="First system step.")

    # Now chain: feed the interpreter's own output back into itself
    out2 = interpreter.infer(context=out1, content="Second system step.")

    o1 = out1.observations[0]
    o2 = out2.observations[0]

    # IDs must increase
    assert o1.id < o2.id

    # Timestamps must increase
    assert o1.timestamp < o2.timestamp

    # Provenance hashes must be non-decreasing
    assert o1.provenance.hash <= o2.provenance.hash

    # Confidence must follow 1/(1+counter)
    assert o1.provenance.confidence == 1 / 2
    assert o2.provenance.confidence == 1 / 3

    # Content must now derive from the *system* observation, not the original user context
    assert o1.content == "Derived: User begins the chain. -> First system step."
    assert o2.content == f"Derived: {o1.content} -> Second system step."

def test_interpreter_depth_limited_chain():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_depth_001",
        "timestamp": ts,
        "source": "user",
        "content": "Start.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_depth_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # Perform a 3-step deterministic chain
    final = interpreter.chain(context=ctx_stream, content="Goal.", depth=3)

    # The final output must be a single-step ObservationStream
    assert len(final.observations) == 1

    last = final.observations[0]

    # Confidence must reflect 3 steps: counter = 3 → confidence = 1/4
    # Chain confidence must reflect 3 steps: (1/2) * (1/3) * (1/4) = 1/24
    expected_conf = (1/2) * (1/3) * (1/4)
    assert last.provenance.confidence == expected_conf


    # Content must reflect 3 deterministic derivations
    assert last.content == (
        "Derived: Derived: Derived: Start. -> Goal. -> Goal. -> Goal."
    )

def test_interpreter_chain_provenance_is_aggregated():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_chainprov_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_chainprov_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # Perform a 3-step chain
    final = interpreter.chain(context=ctx_stream, content="Grow.", depth=3)

    last = final.observations[0]

    # Extract the three intermediate hashes
    # We reconstruct them by running the steps manually
    step1 = interpreter.infer(context=ctx_stream, content="Grow.")
    step2 = interpreter.infer(context=step1, content="Grow.")
    step3 = interpreter.infer(context=step2, content="Grow.")

    h1 = step1.observations[0].provenance.hash
    h2 = step2.observations[0].provenance.hash
    h3 = step3.observations[0].provenance.hash

    # Expected aggregated hash
    expected = hashlib.sha256((h1 + h2 + h3).encode("utf-8")).hexdigest()

    # The final chain output must use the aggregated hash
    assert last.provenance.hash == expected

def test_interpreter_chain_confidence_is_aggregated():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_chainconf_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_chainconf_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # Perform a 3-step chain
    final = interpreter.chain(context=ctx_stream, content="Grow.", depth=3)

    last = final.observations[0]

    # Chain confidence must reflect 3 steps: (1/2) * (1/3) * (1/4) = 1/24
    expected_conf = (1/2) * (1/3) * (1/4)
    assert last.provenance.confidence == expected_conf

def test_interpreter_chain_terminates_on_fixed_point():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_term_001",
        "timestamp": ts,
        "source": "user",
        "content": "Stable.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_term_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # We force a fixed point by giving the same content repeatedly
    final = interpreter.chain(context=ctx_stream, content="Stable.", depth=10)

    last = final.observations[0]

    # The chain should terminate early (before depth=10)
    # Confidence should reflect only the steps actually taken.
    # For a fixed point, only 1 step should occur.
    assert last.provenance.confidence == 1/2

    # Content should reflect only one derivation
    assert last.content == "Derived: Stable. -> Stable."

def test_interpreter_produces_deterministic_two_branch_reasoning_tree():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    # Initial user context
    obs = Observation(**{
        "id": "obs_ctx_tree_001",
        "timestamp": ts,
        "source": "user",
        "content": "User provides a seed for branching.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # 6.3.0: produce a deterministic two-branch reasoning tree
    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Interpreter explores two deterministic branches.",
    )

    # Tree-level structure
    assert tree.id.startswith("tree_")
    assert len(tree.id) > 5  # sanity check

    assert tree.root_context.id == ctx_stream.id
    assert tree.provenance.origin == "system"

    # Must expose exactly two deterministic branches
    assert set(tree.branches.keys()) == {"branch_0001", "branch_0002"}

    branch1 = tree.branches["branch_0001"]
    branch2 = tree.branches["branch_0002"]

    # Each branch must be a valid ObservationStream with a single final observation
    assert isinstance(branch1, ObservationStream)
    assert isinstance(branch2, ObservationStream)
    assert len(branch1.observations) == 1
    assert len(branch2.observations) == 1

    o1 = branch1.observations[0]
    o2 = branch2.observations[0]

    # IDs must be system-scoped and globally monotonic across the tree
    assert branch1.id.startswith("stream_sys_")
    assert branch2.id.startswith("stream_sys_")
    assert o1.id.startswith("obs_sys_")
    assert o2.id.startswith("obs_sys_")
    assert branch1.id < branch2.id
    assert o1.id < o2.id

    # Branch-level outputs must be system-origin and respect existing 6.2 invariants
    assert o1.source == "system"
    assert o2.source == "system"
    assert o1.provenance.origin == "system"
    assert o2.provenance.origin == "system"

    # Tree-level provenance must aggregate both branches deterministically
    h1 = o1.provenance.hash
    h2 = o2.provenance.hash
    c1 = o1.provenance.confidence
    c2 = o2.provenance.confidence

    expected_tree_hash = hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()
    expected_tree_conf = c1 * c2

    assert tree.provenance.hash == expected_tree_hash
    assert tree.provenance.confidence == expected_tree_conf

def test_interpreter_reason_tree_respects_branch_depth():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    # Initial user context
    obs = Observation(**{
        "id": "obs_ctx_tree_depth_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for depth-controlled branching.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_depth_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # 6.3.1: specify branch depth explicitly
    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Branching with controlled depth.",
        branch_depth=3,
    )

    # Tree-level structure
    assert tree.id.startswith("tree_")
    assert len(tree.id) > 5  # sanity check

    assert tree.root_context.id == ctx_stream.id
    assert tree.provenance.origin == "system"

    # Must expose exactly two deterministic branches
    assert set(tree.branches.keys()) == {"branch_0001", "branch_0002"}

    branch1 = tree.branches["branch_0001"]
    branch2 = tree.branches["branch_0002"]

    # Each branch must be a valid ObservationStream with a single final observation
    assert isinstance(branch1, ObservationStream)
    assert isinstance(branch2, ObservationStream)
    assert len(branch1.observations) == 1
    assert len(branch2.observations) == 1

    o1 = branch1.observations[0]
    o2 = branch2.observations[0]

    # IDs must be system-scoped and globally monotonic across the tree
    assert branch1.id.startswith("stream_sys_")
    assert branch2.id.startswith("stream_sys_")
    assert o1.id.startswith("obs_sys_")
    assert o2.id.startswith("obs_sys_")
    assert branch1.id < branch2.id
    assert o1.id < o2.id

    # Branch-level provenance must reflect depth=3
    # Confidence for depth 3: (1/2)*(1/3)*(1/4) = 1/24
    expected_branch_conf = (1/2) * (1/3) * (1/4)
    assert o1.provenance.confidence == expected_branch_conf
    assert o2.provenance.confidence == expected_branch_conf

    # Tree-level provenance must aggregate both branches deterministically
    h1 = o1.provenance.hash
    h2 = o2.provenance.hash
    c1 = o1.provenance.confidence
    c2 = o2.provenance.confidence

    expected_tree_hash = hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()
    expected_tree_conf = c1 * c2

    assert tree.provenance.hash == expected_tree_hash
    assert tree.provenance.confidence == expected_tree_conf

def test_interpreter_reason_tree_exposes_branch_internal_structure():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    # Initial user context
    obs = Observation(**{
        "id": "obs_ctx_tree_struct_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for structured branching.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_struct_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # 6.3.2: branches must expose full internal structure
    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Structured branch reasoning.",
        branch_depth=3,
        expose_internal=True,
    )

    # Tree-level structure
    assert tree.id.startswith("tree_")
    assert len(tree.id) > 5  # sanity check

    assert tree.root_context.id == ctx_stream.id
    assert tree.provenance.origin == "system"

    # Must expose exactly two deterministic branches
    assert set(tree.branches.keys()) == {"branch_0001", "branch_0002"}

    branch1 = tree.branches["branch_0001"]
    branch2 = tree.branches["branch_0002"]

    # NEW: Each branch must now expose all internal steps
    assert isinstance(branch1, list)
    assert isinstance(branch2, list)
    assert len(branch1) == 3
    assert len(branch2) == 3

    # Each element must be an ObservationStream with a single observation
    for step in branch1:
        assert isinstance(step, ObservationStream)
        assert len(step.observations) == 1

    for step in branch2:
        assert isinstance(step, ObservationStream)
        assert len(step.observations) == 1

    # Final step of each branch must match the tree-level provenance aggregation inputs
    final1 = branch1[-1].observations[0]
    final2 = branch2[-1].observations[0]

    # IDs must be globally monotonic across all steps in both branches
    all_ids = [step.observations[0].id for step in branch1 + branch2]
    assert all_ids == sorted(all_ids)

    # Branch-level confidence must still reflect depth=3
    expected_branch_conf = (1/2) * (1/3) * (1/4)
    assert final1.provenance.confidence == expected_branch_conf
    assert final2.provenance.confidence == expected_branch_conf

    # Tree-level provenance must aggregate final step hashes
    h1 = final1.provenance.hash
    h2 = final2.provenance.hash
    expected_tree_hash = hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()
    expected_tree_conf = expected_branch_conf * expected_branch_conf

    assert tree.provenance.hash == expected_tree_hash
    assert tree.provenance.confidence == expected_tree_conf

def test_interpreter_reason_tree_supports_multiple_branches():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_multi_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for multi-branch reasoning.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_multi_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # 6.3.3: request 4 deterministic branches
    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Multi-branch reasoning.",
        branch_depth=2,
        num_branches=4,
        expose_internal=True,
    )

    # Tree-level structure
    assert tree.id.startswith("tree_")
    assert len(tree.id) > 5  # sanity check

    assert tree.root_context.id == ctx_stream.id
    assert tree.provenance.origin == "system"

    # Must expose exactly 4 branches
    assert set(tree.branches.keys()) == {
        "branch_0001",
        "branch_0002",
        "branch_0003",
        "branch_0004",
    }

    # Each branch must expose internal structure (depth=2)
    for key in ["branch_0001", "branch_0002", "branch_0003", "branch_0004"]:
        steps = tree.branches[key]
        assert isinstance(steps, list)
        assert len(steps) == 2
        for step in steps:
            assert isinstance(step, ObservationStream)
            assert len(step.observations) == 1

    # Final observations for provenance aggregation
    finals = [tree.branches[k][-1].observations[0] for k in sorted(tree.branches.keys())]

    # IDs must be globally monotonic across all branches and steps
    all_ids = [step.observations[0].id for k in sorted(tree.branches.keys()) for step in tree.branches[k]]
    assert all_ids == sorted(all_ids)

    # Branch-level confidence for depth=2: (1/2)*(1/3) = 1/6
    expected_branch_conf = (1/2) * (1/3)
    for f in finals:
        assert f.provenance.confidence == expected_branch_conf

    # Tree-level provenance aggregation
    combined_hash = hashlib.sha256(
        "".join(f.provenance.hash for f in finals).encode("utf-8")
    ).hexdigest()

def test_interpreter_reason_tree_selects_deterministic_branch():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_select_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for branch selection.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_select_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    # 6.3.4: deterministic selection among 5 branches
    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Branch selection test.",
        branch_depth=2,
        num_branches=5,
        expose_internal=True,
    )

    # Must expose a selected branch
    assert hasattr(tree, "selected_branch")
    assert tree.selected_branch in tree.branches

    # Deterministic rule:
    # selected branch = branch whose final observation has the smallest hash
    finals = {
        key: tree.branches[key][-1].observations[0].provenance.hash
        for key in tree.branches
    }

    expected = min(finals.items(), key=lambda kv: kv[1])[0]

    assert tree.selected_branch == expected

def test_interpreter_reason_tree_includes_selection_justification():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_justify_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for justification test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_justify_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Justification test.",
        branch_depth=2,
        num_branches=4,
        expose_internal=True,
    )

    # Must include justification
    assert hasattr(tree, "selection_justification")
    just = tree.selection_justification

    # Must include required fields
    assert just["rule"] == "lexicographically_smallest_provenance_hash"
    assert just["selected_branch"] == tree.selected_branch

    # Must include final hash of selected branch
    selected_final_hash = tree.branches[tree.selected_branch][-1].observations[0].provenance.hash
    assert just["selected_branch_final_hash"] == selected_final_hash

    # Must include all branch final hashes in sorted order
    finals = {
        key: tree.branches[key][-1].observations[0].provenance.hash
        for key in tree.branches
    }
    expected_sorted = sorted(finals.items(), key=lambda kv: kv[1])

    assert just["all_branch_final_hashes"] == expected_sorted

def test_interpreter_reason_tree_includes_branch_scores():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_score_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for scoring test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_score_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Scoring test.",
        branch_depth=2,
        num_branches=4,
        expose_internal=True,
    )

    # Must include branch_scores
    assert hasattr(tree, "branch_scores")
    scores = tree.branch_scores

    # Must have one score per branch
    assert set(scores.keys()) == set(tree.branches.keys())

    # Score must be deterministic: int(final_hash, 16)
    for key, score in scores.items():
        final_hash = tree.branches[key][-1].observations[0].provenance.hash
        expected_score = int(final_hash, 16)
        assert score == expected_score

    # Selected branch must have the smallest score
    selected = tree.selected_branch
    min_key = min(scores.items(), key=lambda kv: kv[1])[0]
    assert selected == min_key

def test_interpreter_reason_tree_includes_branch_ranking():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_rank_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for ranking test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_rank_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Ranking test.",
        branch_depth=2,
        num_branches=5,
        expose_internal=True,
    )

    # Must include branch_ranking
    assert hasattr(tree, "branch_ranking")
    ranking = tree.branch_ranking

    # Ranking must be a list of (branch_key, score) pairs
    assert isinstance(ranking, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in ranking)

    # Must include all branches
    assert set(k for k, _ in ranking) == set(tree.branches.keys())

    # Must be sorted by ascending score
    scores = tree.branch_scores
    expected_sorted = sorted(scores.items(), key=lambda kv: kv[1])
    assert ranking == expected_sorted

    # First ranked branch must match selected_branch
    assert ranking[0][0] == tree.selected_branch

def test_interpreter_reason_tree_includes_selected_branch_trace():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_trace_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for trace extraction test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_trace_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Trace extraction test.",
        branch_depth=3,
        num_branches=4,
        expose_internal=True,
    )

    # Must include selected_branch_trace
    assert hasattr(tree, "selected_branch_trace")
    trace = tree.selected_branch_trace

    # Trace must be a list of Observation objects
    assert isinstance(trace, list)
    assert all(isinstance(o, Observation) for o in trace)

    # Trace must match the selected branch's internal structure
    selected = tree.selected_branch
    expected_steps = tree.branches[selected]

    # Flatten expected steps into a list of Observations
    expected_trace = []
    for step_stream in expected_steps:
        expected_trace.extend(step_stream.observations)

    assert trace == expected_trace

def test_interpreter_reason_tree_includes_branch_metadata():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_meta_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for metadata test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_meta_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Metadata test.",
        branch_depth=3,
        num_branches=4,
        expose_internal=True,
    )

    # Must include branch_metadata
    assert hasattr(tree, "branch_metadata")
    meta = tree.branch_metadata

    # Must include metadata for each branch
    assert set(meta.keys()) == set(tree.branches.keys())

    for key, info in meta.items():
        # Required fields
        assert "depth" in info
        assert "num_observations" in info
        assert "final_confidence" in info
        assert "final_hash" in info
        assert "score" in info

        # Validate values
        steps = tree.branches[key]
        final_obs = steps[-1].observations[0]

        assert info["depth"] == len(steps)
        assert info["num_observations"] == sum(len(s.observations) for s in steps)
        assert info["final_confidence"] == final_obs.provenance.confidence
        assert info["final_hash"] == final_obs.provenance.hash
        assert info["score"] == tree.branch_scores[key]

def test_interpreter_reason_tree_includes_deterministic_summary():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_summary_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for summary test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_summary_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Summary test.",
        branch_depth=3,
        num_branches=4,
        expose_internal=True,
    )

    # Must include summary
    assert hasattr(tree, "summary")
    summary = tree.summary

    # Basic structural fields
    assert summary["root_context_id"] == tree.root_context.id
    assert summary["num_branches"] == len(tree.branches)
    assert summary["branch_keys"] == sorted(tree.branches.keys())

    # Selected branch consistency
    assert summary["selected_branch"] == tree.selected_branch
    assert summary["selected_branch_score"] == tree.branch_scores[tree.selected_branch]

    meta = tree.branch_metadata[tree.selected_branch]
    assert summary["selected_branch_depth"] == meta["depth"]
    assert summary["selected_branch_num_observations"] == meta["num_observations"]

    # Provenance consistency
    assert summary["tree_provenance_hash"] != tree.provenance.hash
    assert summary["tree_provenance_confidence"] == tree.provenance.confidence

def test_interpreter_prunes_branches_deterministically():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs = Observation(**{
        "id": "obs_ctx_tree_prune_001",
        "timestamp": ts,
        "source": "user",
        "content": "Seed for pruning test.",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    ctx_stream = ObservationStream.model_validate({
        "id": "stream_ctx_tree_prune_001",
        "observations": [obs],
    })

    interpreter = DeterministicInterpreter()

    tree = interpreter.reason_tree(
        context=ctx_stream,
        content="Pruning test.",
        branch_depth=3,
        num_branches=6,
        expose_internal=True,
        prune_below_rank=2,
    )

    # Only top 2 branches should remain
    assert len(tree.branches) == 2

    # Ranking must reflect only the top 2
    assert len(tree.branch_ranking) == 2

    # Scores must reflect only the top 2
    assert len(tree.branch_scores) == 2

    # Metadata must reflect only the top 2
    assert len(tree.branch_metadata) == 2

    # Summary must reflect pruning
    assert tree.summary["num_branches"] == 2
    assert len(tree.summary["branch_keys"]) == 2

    # Selected branch must be valid
    assert tree.selected_branch in tree.branches
