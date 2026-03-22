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
