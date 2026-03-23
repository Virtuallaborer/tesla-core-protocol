import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from tesla_core_protocol.models import Observation, ObservationStream


def test_observation_stream_enforces_monotonic_timestamps():
    ts = datetime.utcnow()

    obs1 = Observation(**{
        "id": "obs_stream_001",
        "timestamp": ts,
        "source": "user",
        "content": "First in stream",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_stream_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "Second in stream",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Should succeed: strictly increasing timestamps
    stream = ObservationStream.model_validate({
        "id": "stream_001",
        "observations": [obs1, obs2],
    })

    # Now create a stream with a regression → must fail
    obs3 = Observation(**{
        "id": "obs_stream_003",
        "timestamp": ts - timedelta(seconds=1),
        "source": "user",
        "content": "Out-of-order event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_002",
            "observations": [obs1, obs3],
        })


def test_stream_timestamps_must_not_regress():
    ts = datetime.utcnow()

    obs1 = Observation(**{
        "id": "obs_ctx_stream_regress_001",
        "timestamp": ts,
        "source": "user",
        "content": "First event in stream",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    past_time = ts - timedelta(seconds=10)

    obs2 = Observation(**{
        "id": "obs_ctx_stream_regress_002",
        "timestamp": past_time,
        "source": "user",
        "content": "Second event in stream (regressing)",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_ctx_regress_001",
            "observations": [obs1, obs2],
        })


def test_stream_timestamps_must_not_be_equal():
    ts = datetime.utcnow()

    obs1 = Observation(**{
        "id": "obs_ctx_stream_equal_001",
        "timestamp": ts,
        "source": "user",
        "content": "First event in stream",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_ctx_stream_equal_002",
        "timestamp": ts,  # same timestamp
        "source": "user",
        "content": "Second event in stream (same ts)",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_ctx_equal_001",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_invalid_source_transition():
    ts = datetime.utcnow()

    # First observation: system-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_001",
        "timestamp": ts,
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # Second observation: user-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "User message",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_source_transition",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_environment_to_memory_transition():
    ts = datetime.utcnow()

    # TEST 29 First observation: environment-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_env_001",
        "timestamp": ts,
        "source": "environment",
        "content": "Sensor reading",
        "provenance": {
            "hash": "a" * 32,
            "origin": "sensor",
            "confidence": 1.0,
        },
    })

    # TEST 30 Second observation: memory-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_mem_001",
        "timestamp": ts + timedelta(seconds=1),
        "source": "memory",
        "content": "Recalled memory",
        "provenance": {
            "hash": "b" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_env_to_memory",
            "observations": [obs1, obs2],
        })
#TEST 31
def test_stream_rejects_user_to_tool_transition():
    ts = datetime.utcnow()

    # First observation: user-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_user_001",
        "timestamp": ts,
        "source": "user",
        "content": "User action",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Second observation: tool-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_tool_001",
        "timestamp": ts + timedelta(seconds=1),
        "source": "tool",
        "content": "Tool response",
        "provenance": {
            "hash": "b" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_user_to_tool",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_tool_to_memory_transition():
    ts = datetime.utcnow()

    # First observation: tool-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_tool_002",
        "timestamp": ts,
        "source": "tool",
        "content": "Tool output",
        "provenance": {
            "hash": "a" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # Second observation: memory-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_mem_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "memory",
        "content": "Memory recall",
        "provenance": {
            "hash": "b" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_tool_to_memory",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_system_to_memory_transition():
    ts = datetime.utcnow()

    # First observation: system-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_system_003",
        "timestamp": ts,
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # Second observation: memory-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_mem_003",
        "timestamp": ts + timedelta(seconds=1),
        "source": "memory",
        "content": "Memory recall",
        "provenance": {
            "hash": "b" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_system_to_memory",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_memory_to_system_transition():
    ts = datetime.utcnow()

    # First observation: memory-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_mem_004",
        "timestamp": ts,
        "source": "memory",
        "content": "Memory recall",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # Second observation: system-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_system_004",
        "timestamp": ts + timedelta(seconds=1),
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "b" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_memory_to_system",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_tool_to_system_transition():
    ts = datetime.utcnow()

    # First observation: tool-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_tool_005",
        "timestamp": ts,
        "source": "tool",
        "content": "Tool output",
        "provenance": {
            "hash": "a" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # Second observation: system-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_system_005",
        "timestamp": ts + timedelta(seconds=1),
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "b" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_tool_to_system",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_environment_to_system_transition():
    ts = datetime.utcnow()

    # First observation: environment-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_env_006",
        "timestamp": ts,
        "source": "environment",
        "content": "Environmental signal",
        "provenance": {
            "hash": "a" * 32,
            "origin": "environment",
            "confidence": 1.0,
        },
    })

    # Second observation: system-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_system_006",
        "timestamp": ts + timedelta(seconds=1),
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "b" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_environment_to_system",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_user_to_system_transition():
    ts = datetime.utcnow()

    # First observation: user-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_user_007",
        "timestamp": ts,
        "source": "user",
        "content": "User action",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Second observation: system-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_system_007",
        "timestamp": ts + timedelta(seconds=1),
        "source": "system",
        "content": "System event",
        "provenance": {
            "hash": "b" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_user_to_system",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_memory_to_user_transition():
    ts = datetime.utcnow()

    # First observation: memory-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_memory_008",
        "timestamp": ts,
        "source": "memory",
        "content": "Recalled memory",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # Second observation: user-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_user_008",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "User action",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_memory_to_user",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_tool_to_user_transition():
    ts = datetime.utcnow()

    # First observation: tool-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_tool_009",
        "timestamp": ts,
        "source": "tool",
        "content": "Tool output",
        "provenance": {
            "hash": "a" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # Second observation: user-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_user_009",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "User action",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_tool_to_user",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_memory_to_tool_transition():
    ts = datetime.utcnow()

    # First observation: memory-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_memory_010",
        "timestamp": ts,
        "source": "memory",
        "content": "Recalled memory",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # Second observation: tool-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_tool_010",
        "timestamp": ts + timedelta(seconds=1),
        "source": "tool",
        "content": "Tool activation",
        "provenance": {
            "hash": "b" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_memory_to_tool",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_memory_to_environment_transition():
    ts = datetime.utcnow()

    # First observation: memory-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_memory_011",
        "timestamp": ts,
        "source": "memory",
        "content": "Recalled memory",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0,
        },
    })

    # Second observation: environment-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_environment_011",
        "timestamp": ts + timedelta(seconds=1),
        "source": "environment",
        "content": "Environmental reading",
        "provenance": {
            "hash": "b" * 32,
            "origin": "environment",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_memory_to_environment",
            "observations": [obs1, obs2],
        })

def test_stream_rejects_tool_to_environment_transition():
    ts = datetime.utcnow()

    # First observation: tool-generated
    obs1 = Observation(**{
        "id": "obs_stream_src_tool_013",
        "timestamp": ts,
        "source": "tool",
        "content": "Tool activation event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "tool",
            "confidence": 1.0,
        },
    })

    # Second observation: environment-generated (invalid adjacency)
    obs2 = Observation(**{
        "id": "obs_stream_src_environment_013",
        "timestamp": ts + timedelta(seconds=1),
        "source": "environment",
        "content": "Environmental reading",
        "provenance": {
            "hash": "b" * 32,
            "origin": "environment",
            "confidence": 1.0,
        },
    })

    # This adjacency should be rejected by Subsystem 4
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid_tool_to_environment",
            "observations": [obs1, obs2],
        })
