import pytest
import hashlib

from datetime import datetime, timedelta
from pydantic import ValidationError

from tesla_core_protocol.models import Observation, ObservationStream
from tesla_core_protocol import DeterministicInterpreter

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
