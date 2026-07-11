from dataclasses import dataclass
import hashlib

@dataclass
class AgentTemporalFieldLatticeSurfaces:
    """
    Phase 14.15–14.20 lattice-level surfaces.
    Phase 14.21+ will extend this file.
    """

    agentic_temporal_field_full_synthesis_lattice_hash: str | None = None
    agentic_temporal_field_lattice_coherence_hash: str | None = None
    agentic_temporal_field_lattice_stability_hash: str | None = None

    # Phase 14.21+ surfaces
    agentic_temporal_field_lattice_progression_hash: str | None = None

    def compute_lattice_progression_surface(
        self,
        full_synthesis_lattice_hash: str,
        lattice_coherence_hash: str,
        lattice_stability_hash: str,
        semantic_nucleus_identity_hash: str,
    ) -> str:

        lattice_progression_input = "|".join(
            [
                full_synthesis_lattice_hash,
                lattice_coherence_hash,
                lattice_stability_hash,
                semantic_nucleus_identity_hash,
            ]
        )

        self.agentic_temporal_field_lattice_progression_hash = hashlib.sha256(
            lattice_progression_input.encode("utf-8")
        ).hexdigest()

        return self.agentic_temporal_field_lattice_progression_hash
