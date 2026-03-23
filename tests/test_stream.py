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

def test_stream_id_must_be_well_formed():
    ts = datetime.utcnow()

    valid_obs = Observation(**{
        "id": "obs_stream_id_001",
        "timestamp": ts,
        "source": "user",
        "content": "Stream ID invariant probe",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Should succeed: well-formed stream id
    stream_ok = ObservationStream.model_validate({
        "id": "stream_ctx_001_valid",
        "observations": [valid_obs],
    })
    assert stream_ok.id == "stream_ctx_001_valid"

    # Missing 'stream_' prefix → must fail
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "ctx_001_invalid_prefix",
            "observations": [valid_obs],
        })

    # Invalid characters in suffix → must fail
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_invalid-characters",
            "observations": [valid_obs],
        })

    # Too long → must fail
    long_suffix = "x" * 60
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_" + long_suffix,
            "observations": [valid_obs],
        })


def test_stream_must_not_be_empty():
    # A stream with no observations must be rejected
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_empty_001",
            "observations": [],
        })

def test_stream_id_must_be_globally_unique():
    ts = datetime.utcnow()

    obs = Observation(**{
        "id": "obs_stream_unique_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # First stream with this ID should succeed
    stream1 = ObservationStream.model_validate({
        "id": "stream_unique_test_001",
        "observations": [obs],
    })

    # Second stream with the same ID must fail
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_unique_test_001",
            "observations": [obs],
        })

def test_stream_must_not_contain_duplicate_observation_instances():
    ts = datetime.utcnow()

    obs = Observation(**{
        "id": "obs_stream_instance_unique_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Attempt to reuse the same Observation instance twice
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_instance_dup_001",
            "observations": [obs, obs],
        })

def test_stream_observation_ids_must_be_strictly_increasing():
    ts = datetime.utcnow()

    obs1 = Observation(**{
        "id": "obs_alpha_001",
        "timestamp": ts,
        "source": "user",
        "content": "First event",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_alpha_000",  # lexicographically smaller
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "Second event",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Stream must reject ID regression
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_id_regression_001",
            "observations": [obs1, obs2],
        })

def test_stream_must_not_contain_duplicate_timestamps_anywhere():
    ts = datetime.utcnow()

    obs1 = Observation(**{
        "id": "obs_ts_dup_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_ts_dup_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_ts_dup_003",
        "timestamp": ts,  # duplicate timestamp, non-adjacent
        "source": "user",
        "content": "Event 3",
        "provenance": {
            "hash": "c" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Stream must reject duplicate timestamps anywhere in the sequence
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_ts_dup_001",
            "observations": [obs1, obs2, obs3],
        })

def test_stream_provenance_hashes_must_be_strictly_increasing():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_hash_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,  # lexicographically smaller
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_hash_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "Event 2",
        "provenance": {
            "hash": "9" * 32,  # lexicographically larger
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_hash_003",
        "timestamp": ts + timedelta(seconds=2),
        "source": "user",
        "content": "Event 3",
        "provenance": {
            "hash": "0" * 32,  # regression
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Stream must reject provenance hash regression
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_hash_regression_001",
            "observations": [obs1, obs2, obs3],
        })

def test_stream_provenance_confidence_must_be_non_decreasing():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_conf_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 0.9,
        },
    })

    obs2 = Observation(**{
        "id": "obs_conf_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "user",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_conf_003",
        "timestamp": ts + timedelta(seconds=2),
        "source": "user",
        "content": "Event 3",
        "provenance": {
            "hash": "c" * 32,
            "origin": "user",
            "confidence": 0.8,  # regression
        },
    })

    # Stream must reject confidence regression
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_conf_regression_001",
            "observations": [obs1, obs2, obs3],
        })

def test_stream_provenance_origin_must_be_coherent():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_origin_001",
        "timestamp": ts,
        "source": "environment",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "environment",  # valid
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_origin_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "environment",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "sensor",  # also valid
            "confidence": 1.0,
        },
    })

    # Both observations are individually valid.
    # The source transition environment → environment is allowed.
    # But the stream must reject mixed provenance origins.
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_origin_incoherent_001",
            "observations": [obs1, obs2],
        })

def test_stream_source_must_be_dominant_class():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_source_001",
        "timestamp": ts,
        "source": "environment",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "environment",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_source_002",
        "timestamp": ts + timedelta(seconds=1),
        "source": "environment",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "sensor",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_source_003",
        "timestamp": ts + timedelta(seconds=2),
        "source": "system",  # different source, but individually valid
        "content": "Event 3",
        "provenance": {
            "hash": "c" * 32,
            "origin": "system",
            "confidence": 1.0,
        },
    })

    # All observations are individually valid.
    # environment → environment is allowed.
    # environment → system is forbidden by adjacency,
    # but we want the stream-level invariant to catch this BEFORE adjacency.
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_source_incoherent_001",
            "observations": [obs1, obs2, obs3],
        })

def test_stream_temporal_gap_must_not_exceed_limit():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_gap_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_gap_002",
        "timestamp": ts + timedelta(seconds=30),
        "source": "user",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_gap_003",
        "timestamp": ts + timedelta(seconds=120),  # gap of 90 seconds
        "source": "user",
        "content": "Event 3",
        "provenance": {
            "hash": "c" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Gap between obs2 and obs3 is 90 seconds → should fail
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_gap_violation_001",
            "observations": [obs1, obs2, obs3],
        })

def test_stream_total_duration_must_not_exceed_window():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    obs1 = Observation(**{
        "id": "obs_window_001",
        "timestamp": ts,
        "source": "user",
        "content": "Event 1",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs2 = Observation(**{
        "id": "obs_window_002",
        "timestamp": ts + timedelta(seconds=100),
        "source": "user",
        "content": "Event 2",
        "provenance": {
            "hash": "b" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    obs3 = Observation(**{
        "id": "obs_window_003",
        "timestamp": ts + timedelta(seconds=400),  # total duration = 400 seconds
        "source": "user",
        "content": "Event 3",
        "provenance": {
            "hash": "c" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    # Total duration = 400 seconds → should fail (limit is 300)
    with pytest.raises(ValidationError):
        ObservationStream.model_validate({
            "id": "stream_window_violation_001",
            "observations": [obs1, obs2, obs3],
        })





