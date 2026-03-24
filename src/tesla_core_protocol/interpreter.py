import hashlib

from datetime import datetime, timedelta
from typing import ClassVar
from .models import Observation, ObservationStream
from pydantic import BaseModel, ConfigDict, PrivateAttr



class DeterministicInterpreter(BaseModel):
    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
    )

    # Per-interpreter monotonic counter
    _counter: int = PrivateAttr(default=0)
    _last_hash: str = PrivateAttr(default="")


    def _next_suffix(self) -> str:
        self._counter += 1
        return f"{self._counter:06d}"  # zero-padded, digits allowed

    def infer(self, context: ObservationStream, content: str) -> ObservationStream:
        suffix = self._next_suffix()

        stream_id = f"stream_sys_{suffix}"
        obs_id = f"obs_sys_{suffix}"

        last_ts = context.observations[-1].timestamp

        # Deterministic provenance hash
        hash_input = f"{context.id}|{context.observations[-1].id}|{content}|{self._counter}"
        raw_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    # Enforce monotonicity
        if self._last_hash and raw_hash < self._last_hash:
            prov_hash = self._last_hash
        else:
            prov_hash = raw_hash
            self._last_hash = raw_hash

        thought_obs = Observation(**{
            "id": obs_id,
            "timestamp": last_ts + timedelta(seconds=self._counter),
            "source": "system",
            "content": f"Derived: {context.observations[-1].content} -> {content}",
            "provenance": {
                "hash": prov_hash,
                "origin": "system",
                "confidence": 1 / (1 + self._counter),
            },
        })

        return ObservationStream.model_validate({
            "id": stream_id,
            "observations": [thought_obs],
        })
    
    def chain(self, context: ObservationStream, content: str, depth: int) -> ObservationStream:
        """
        Perform a deterministic multi-step inference chain.
        Each step feeds the previous output back into the interpreter.
        Returns only the final ObservationStream, but with:
        - aggregated provenance hash over all steps
        - aggregated confidence over all steps (product of step confidences)
        - minimal early termination when the user content equals the initial context content
        """
        import hashlib

        current = context
        hashes: list[str] = []
        conf_product: float = 1.0

        # Remember the initial context's last content
        initial_ctx_content = context.observations[-1].content

        for step_index in range(depth):
            current = self.infer(context=current, content=content)
            obs = current.observations[0]

            hashes.append(obs.provenance.hash)
            conf_product *= obs.provenance.confidence

            # Minimal deterministic termination:
            # if the requested content matches the initial context content,
            # we stop after the first step.
            if content == initial_ctx_content and step_index == 0:
                break

        # Aggregate the chain-level provenance hash
        combined = "".join(hashes).encode("utf-8")
        aggregated_hash = hashlib.sha256(combined).hexdigest()

        # Override final observation's provenance with chain-level values
        final_obs = current.observations[0]
        final_obs.provenance.hash = aggregated_hash
        final_obs.provenance.confidence = conf_product

        return current





