import pytest
from datetime import datetime
from tesla_core_protocol.models import Observation, Provenance
import datetime as dt

#Test 1 for the Observation model and its interaction with Provenance, including validation rules and error handling.

def test_create_minimal_observation():
    prov = Provenance(
        hash="a" * 32,
        origin="user",
        confidence=1.0,
    )

    obs = Observation.model_validate({
        "id": "obs_001",
        "timestamp": datetime.utcnow(),
        "source": "user",
        "content": "Hello TESLA",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0,
        },
    })

    assert obs.id == "obs_001"
    assert obs.source == "user"
    assert obs.provenance.origin == "user"
    
#Test 2: Validation of the 'source' field in the Observation model

def test_observation_rejects_invalid_source():
    prov = Provenance(
        hash="a" * 32,
        origin="test",
        confidence=1.0
    )

    from pydantic import ValidationError

    with pytest.raises(ValidationError):

        Observation.model_validate({
            "id": "obs_002",
            "timestamp": datetime.utcnow(),
            "source": "banana",  # invalid
            "content": "Invalid source test",
            "provenance": {
            "hash": "a" * 32,
            "origin": "test",
            "confidence": 1.0
            }
        })
#Test 3: Validation of the 'timestamp' field in the Observation model, ensuring that it must be a datetime object and cannot be set to a future time.
def test_observation_requires_datetime_timestamp():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_003",
            "timestamp": "not-a-datetime",
            "source": "user",
            "content": "Invalid timestamp test",
            "provenance": {
                "hash": "a" * 32,
                "origin": "test",
                "confidence": 1.0
            }
        })
#Test 4: Validation of the 'confidence' field in the Provenance model, ensuring that it must be a float between 0 and 1, and that values outside this range raise appropriate errors.
def test_observation_id_must_start_with_obs_prefix():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "invalid_001",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "Testing invalid ID",
            "provenance": {
                "hash": "a" * 32,
                "origin": "test",
                "confidence": 1.0
            
            }
        })
#Test 5: Validation of the 'content' field in the Observation model
def test_provenance_confidence_must_be_between_0_and_1():
    from pydantic import ValidationError

    # Too low
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "a" * 32,
            "origin": "test",
            "confidence": -0.1
        })

    # Too high
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "a" * 32,
            "origin": "test",
            "confidence": 1.1
        })
#Test 6: Validation of the 'id' field in the Observation model
def test_observation_timestamp_cannot_be_in_future():
    from pydantic import ValidationError
    from datetime import datetime, timedelta

    future_time = datetime.utcnow() + timedelta(days=1)

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_010",
            "timestamp": future_time,
            "source": "user",
            "content": "Future timestamp test",
            "provenance": {
                "hash": "a" * 32,
                "origin": "test",
                "confidence": 1.0
            }
        })
#Test 7: Validation of the 'content' field in the Observation model
def test_observation_content_must_not_be_empty():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_011",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "",
            "provenance": {
                "hash": "a" * 32,
                "origin": "test",
                "confidence": 1.0
            }
        })
#Test 8: Validation of the 'hash' and 'origin' fields in the Provenance model, ensuring that they must be non-empty strings and that invalid values raise appropriate errors.
def test_provenance_hash_must_be_non_empty_and_well_formed():
    from pydantic import ValidationError

    # Empty hash
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "",
            "origin": "test",
            "confidence": 1.0
        })

    # Whitespace-only hash
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "   ",
            "origin": "test",
            "confidence": 1.0
        })

    # Malformed hash (invalid characters)
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "not@valid#hash!",
            "origin": "test",
            "confidence": 1.0
        })
#Test 9: Validation of the 'origin' field in the Provenance model,
def test_provenance_origin_must_be_well_formed():
    from pydantic import ValidationError

    # Empty origin
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "a" * 32,
            "origin": "",
            "confidence": 1.0
        })

    # Whitespace-only origin
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "a" * 32,
            "origin": "   ",
            "confidence": 1.0
        })

    # Invalid characters
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "a" * 32,
            "origin": "bad-origin!",
            "confidence": 1.0
        })

    # Uppercase should fail (we enforce lowercase)
    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": "abc123",
            "origin": "TEST",
            "confidence": 1.0
        })
#Test 10: Cross-field validation rules in the Observation model, such as ensuring that if the source is "memory"
def test_observation_memory_source_requires_memory_or_system_origin():
    from pydantic import ValidationError

    # Invalid: source=memory but origin is something else
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_020",
            "timestamp": datetime.utcnow(),
            "source": "memory",
            "content": "Testing cross-field rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",  # invalid
                "confidence": 1.0
            }
        })

    # Valid: origin = memory
    obs1 = Observation.model_validate({
        "id": "obs_021",
        "timestamp": datetime.utcnow(),
        "source": "memory",
        "content": "Valid case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0
        }
    })
    assert obs1.provenance.origin == "memory"

    # Valid: origin = system
    obs2 = Observation.model_validate({
        "id": "obs_022",
        "timestamp": datetime.utcnow(),
        "source": "memory",
        "content": "Valid case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "system",
            "confidence": 1.0
        }
    })
    assert obs2.provenance.origin == "system"
#Test 11: Cross-field validation rules in the Observation model, such as ensuring that if the source is "system", the origin must be "system".
def test_observation_memory_source_requires_memory_or_system_origin():
    from pydantic import ValidationError

    # Invalid: source=memory but origin is something else
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_020",
            "timestamp": datetime.utcnow(),
            "source": "memory",
            "content": "Testing cross-field rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",  # invalid
                "confidence": 1.0
            }
        })

    # Valid: origin = memory
    obs1 = Observation.model_validate({
        "id": "obs_021",
        "timestamp": datetime.utcnow(),
        "source": "memory",
        "content": "Valid case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "memory",
            "confidence": 1.0
        }
    })
    assert obs1.provenance.origin == "memory"

    # Valid: origin = system
    obs2 = Observation.model_validate({
        "id": "obs_022",
        "timestamp": datetime.utcnow(),
        "source": "memory",
        "content": "Valid case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "system",
            "confidence": 1.0
        }
    })
    assert obs2.provenance.origin == "system"

def test_observation_tool_source_requires_matching_origin():
    from pydantic import ValidationError

    # Invalid: source=tool but origin does not match tool name
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_030",
            "timestamp": datetime.utcnow(),
            "source": "tool",
            "content": "Testing tool-origin rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "wrongtool",
                "confidence": 1.0
            }
        })

    # Valid: origin matches tool name
    obs = Observation.model_validate({
        "id": "obs_031",
        "timestamp": datetime.utcnow(),
        "source": "tool",
        "content": "Valid tool-origin case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "tool",
            "confidence": 1.0
        }
    })
    assert obs.provenance.origin == "tool"

#Test 12: Validation of the 'embedding' field in the Observation model, ensuring that it must be a list of floats and that invalid values raise appropriate errors.

def test_observation_environment_source_requires_sensor_or_environment_origin():
    from pydantic import ValidationError

    # Invalid: source=environment but origin is something else
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_040",
            "timestamp": datetime.utcnow(),
            "source": "environment",
            "content": "Testing environment-origin rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",  # invalid
                "confidence": 1.0
            }
        })

    # Valid: origin = sensor
    obs1 = Observation.model_validate({
        "id": "obs_041",
        "timestamp": datetime.utcnow(),
        "source": "environment",
        "content": "Valid environment-origin case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "sensor",
            "confidence": 1.0
        }
    })
    assert obs1.provenance.origin == "sensor"

    # Valid: origin = environment
    obs2 = Observation.model_validate({
        "id": "obs_042",
        "timestamp": datetime.utcnow(),
        "source": "environment",
        "content": "Valid environment-origin case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "environment",
            "confidence": 1.0
        }
    })
    assert obs2.provenance.origin == "environment"

    #Test 13: Create an observation with a tool source but mismatched provenance origin

def test_observation_system_source_requires_system_origin():
    from pydantic import ValidationError

    # Invalid: source=system but origin is something else
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_050",
            "timestamp": datetime.utcnow(),
            "source": "system",
            "content": "Testing system-origin rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",  # invalid
                "confidence": 1.0
            }
        })

    # Valid: origin = system
    obs = Observation.model_validate({
        "id": "obs_051",
        "timestamp": datetime.utcnow(),
        "source": "system",
        "content": "Valid system-origin case",
        "provenance": {
            "hash": "a" * 32,
            "origin": "system",
            "confidence": 1.0
        }
    })
    assert obs.provenance.origin == "system"

    from pydantic import ValidationError

def test_user_source_requires_user_origin_ok():
    obs = Observation.model_validate(
        {
            "id": "obs_user_ok",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "User said something",
            "provenance": {
                "hash": "a" * 64,
                "origin": "user",
                "confidence": 0.9,
            },
        }
    )
    assert obs.provenance.origin == "user"

    
from pydantic import ValidationError

def test_user_source_rejects_non_user_origin():
    with pytest.raises(ValidationError):
        Observation.model_validate(
            {
                "id": "obs_user_bad_origin",
                "timestamp": dt.datetime.utcnow().isoformat(),
                "source": "user",
                "content": "User said something",
                "provenance": {
                    "hash": "b" * 64,
                    "origin": "system",  # not allowed for user source
                    "confidence": 0.9,
                },
            }
        )

def test_observation_content_must_not_be_whitespace_only():
    from pydantic import ValidationError
    from datetime import datetime

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_060",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "   ",  # whitespace-only → invalid
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_id_must_be_well_formed_after_prefix():
    from pydantic import ValidationError
    from datetime import datetime

    # Invalid: contains uppercase + punctuation
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_Invalid-ID!",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "Testing malformed ID",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_timestamp_must_not_be_before_unix_epoch():
    from pydantic import ValidationError
    from datetime import datetime

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_070",
            "timestamp": datetime(1900, 1, 1),  # pre-epoch → invalid
            "source": "user",
            "content": "Testing pre-epoch timestamp",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_content_must_not_exceed_max_length():
    from pydantic import ValidationError
    from datetime import datetime

    too_long = "a" * 10001  # 10,001 characters → invalid

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_080",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": too_long,
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_provenance_hash_must_not_exceed_max_length():
    from pydantic import ValidationError

    too_long_hash = "a" * 257  # 257 characters → invalid

    with pytest.raises(ValidationError):
        Provenance.model_validate({
            "hash": too_long_hash,
            "origin": "user",
            "confidence": 0.9,
        })

def test_observation_id_must_be_unique():
    from datetime import datetime
    from pydantic import ValidationError

    # First creation should succeed
    Observation.model_validate({
        "id": "obs_unique_001",
        "timestamp": datetime.utcnow(),
        "source": "user",
        "content": "First instance",
        "provenance": {
            "hash": "a" * 32,
            "origin": "user",
            "confidence": 1.0
        }
    })

    # Second creation with same ID should fail
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_unique_001",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "Duplicate instance",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_timestamp_must_be_timezone_naive():
    from pydantic import ValidationError
    from datetime import datetime, timezone

    # Invalid: timezone-aware datetime
    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_tz_001",
            "timestamp": datetime.now(timezone.utc),  # tz-aware → invalid
            "source": "user",
            "content": "Testing timezone rule",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_id_must_not_exceed_max_length():
    from pydantic import ValidationError
    from datetime import datetime

    too_long_id = "obs_" + "a" * 61  # total length = 65 → invalid

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": too_long_id,
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "Testing id max length",
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0,
            },
        })

def test_provenance_hash_must_have_minimum_length():
    from pydantic import ValidationError
    from datetime import datetime

    # Too short: only 6 characters
    short_hash = "abc123"

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_hash_min_001",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": "Testing minimum hash length",
            "provenance": {
                "hash": short_hash,
                "origin": "user",
                "confidence": 1.0
            }
        })

def test_observation_content_must_be_utf8_encodable():
    from pydantic import ValidationError
    from datetime import datetime

    # Invalid: unpaired surrogate (cannot be UTF-8 encoded)
    bad_content = "Hello \ud800 World"

    with pytest.raises(ValidationError):
        Observation.model_validate({
            "id": "obs_utf8_001",
            "timestamp": datetime.utcnow(),
            "source": "user",
            "content": bad_content,
            "provenance": {
                "hash": "a" * 32,
                "origin": "user",
                "confidence": 1.0,
            },
        })










