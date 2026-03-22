from datetime import datetime
from models import Observation, Provenance

obs = Observation(
    id="obs_001",
    timestamp=datetime.utcnow(),
    source="user",
    content="User asked about TESLA Core Protocol.",
    embedding=[0.1, 0.2, 0.3],
    provenance=Provenance(
        hash="dummy_hash",
        signature=None,
        origin="cli_demo",
        confidence=0.9
    ),
    context_window=[]
)

print(obs.model_dump_json(indent=2, sort_keys=True))
