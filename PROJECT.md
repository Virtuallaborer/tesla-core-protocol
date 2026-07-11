# 📁 **PROJECT.md — UPDATED July 2026  
### *Agent Module & Test Suite File Structure (Authoritative — July 2026)*

---

## **Agent Module Structure (Phases 9–16)**  
To maintain architectural hygiene and prevent monolithic files, TESLA uses a modular agent surface layout:

```
src/tesla_core_protocol/agent/
    __init__.py
    agent_identity.py
    agent_temporal_identity.py
    agent_temporal_field.py
    agent_temporal_field_lattice.py
    agent_temporal_field_dynamics.py
```

### **Purpose of Each File**

- **agent_identity.py**  
  Phase 9–10 identity surfaces.

- **agent_temporal_identity.py**  
  Phase 11–12 temporal identity surfaces.

- **agent_temporal_field.py**  
  Phase 13 + early Phase 14 temporal‑field surfaces.

- **agent_temporal_field_lattice.py**  
  Phase 14.15–14.30 lattice‑level surfaces.

- **agent_temporal_field_dynamics.py**  
  Phase 15+ temporal‑field autonomy and dynamics.

### **Minimal `__init__.py`**

```python
from .agent_identity import AgentIdentitySurfaces
from .agent_temporal_identity import AgentTemporalIdentitySurfaces
from .agent_temporal_field import AgentTemporalFieldSurfaces
from .agent_temporal_field_lattice import AgentTemporalFieldLatticeSurfaces
from .agent_temporal_field_dynamics import AgentTemporalFieldDynamicsSurfaces
```

### **Surface Containers (not monoliths)**

Each file defines a dataclass that holds only the surfaces relevant to that conceptual layer.

Example:

```python
# agent_temporal_field.py
from dataclasses import dataclass

@dataclass
class AgentTemporalFieldSurfaces:
    agentic_temporal_field_gradient_hash: str | None = None
    agentic_temporal_field_curvature_hash: str | None = None
    # ...
```

```python
# agent_temporal_field_lattice.py
from dataclasses import dataclass

@dataclass
class AgentTemporalFieldLatticeSurfaces:
    agentic_temporal_field_full_synthesis_lattice_hash: str | None = None
    agentic_temporal_field_lattice_coherence_hash: str | None = None
    agentic_temporal_field_lattice_stability_hash: str | None = None
    # Phase 14.21+ surfaces extend here
```

This ensures:

- files stay under ~1000 lines  
- invariants remain isolated  
- future phases never require retroactive splitting  

---

## **Test Suite Structure (Phases 3–16)**

```
tests/
    test_agentic_identity.py                 # Phases 9–14.20 (frozen)
    test_agentic_temporal_identity.py        # Phases 11–12
    test_agentic_temporal_field.py           # Phase 13–early 14
    test_agentic_temporal_field_lattice.py   # Phase 14.15+
    test_agentic_temporal_field_dynamics.py  # Phase 15+
```

### **Purpose of Each Test File**

- **test_agentic_identity.py**  
  Canonical record of identity surfaces through Phase 14.20.

- **test_agentic_temporal_identity.py**  
  Temporal identity invariants.

- **test_agentic_temporal_field.py**  
  Temporal‑field invariants (Phase 13–early 14).

- **test_agentic_temporal_field_lattice.py**  
  Lattice‑level invariants (Phase 14.15–14.30).

- **test_agentic_temporal_field_dynamics.py**  
  Temporal‑field autonomy (Phase 15+).

### **Phase 14.21+ Test Entry Point**

```python
# tests/test_agentic_temporal_field_lattice.py

def test_agentic_temporal_field_lattice_progression_surface_is_deterministic_and_stability_preserving():
    ...
```

This keeps the identity test file frozen and prevents further growth beyond 6100 lines.

---

# 🧭 **Architectural Map (Phases 9–16)**  
### *Identity → Temporal Identity → Field → Lattice → Dynamics*

| Layer | Phases | Code Location | Test Location |
|------|--------|----------------|----------------|
| Identity | 9–10 | agent_identity.py | test_agentic_identity.py |
| Temporal Identity | 11–12 | agent_temporal_identity.py | test_agentic_temporal_identity.py |
| Temporal Field | 13–early 14 | agent_temporal_field.py | test_agentic_temporal_field.py |
| Temporal Field Lattice | 14.15–14.30 | agent_temporal_field_lattice.py | test_agentic_temporal_field_lattice.py |
| Temporal Field Dynamics | 15+ | agent_temporal_field_dynamics.py | test_agentic_temporal_field_dynamics.py |

This is the **canonical architectural map** going forward.

---

Patrick — perfect.  
We’ll close this session by giving you **everything you asked for**, clean, structured, and ready for a fresh next session:

1. **TESLA_PROTOCOL.md (full authoritative spec through Phase 14.20)**  
2. **README.md (updated, concise, external‑facing)**  
3. **Exact skeletons** for:  
   - `agent_temporal_field_lattice.py`  
   - `test_agentic_temporal_field_lattice.py`  

All of this is written to drop directly into your repo so Phase 14.21 can begin cleanly.

---

# 📘 **TESLA_PROTOCOL.md (Authoritative — July 2026)**  
### *Updated through Phase 14.20 — 173 Passing Tests*

This is your **canonical protocol specification**.  
It replaces your older TESLA_PROTOCOL.md entirely.

---

# **TESLA Core Protocol**  
A deterministic reasoning substrate built on the idea that truth emerges from **structure**, **provenance**, and **temporal continuity**.  
TESLA evolves through invariant‑driven development following the **3‑6‑9 progression**.

---

## **1. Core Primitives**

TESLA defines four foundational Pydantic v2 models:

- Provenance  
- Observation  
- ObservationStream  
- ReasoningTree  

All invariants below are enforced by the test suite.

---

## **2. Provenance Invariants**

### **2.1 Hash**
- lowercase hex  
- length 32–256  
- non‑empty  
- non‑decreasing within a stream  
- deterministic SHA‑256  
- monotonic carryover  
- chain‑level hash = SHA256(h₁ + h₂ + … + hₙ)

### **2.2 Origin**
- lowercase `[a-z0-9_]`  
- non‑empty  
- must match source→origin mapping  
- coherent across entire stream

### **2.3 Confidence**
- float ∈ [0.0, 1.0]  
- non‑decreasing within a stream  
- interpreter confidence = `1 / (1 + counter)`  
- chain‑level confidence = product of step confidences

---

## **3. Observation Invariants**

### **3.1 Timestamp**
- strict `datetime`  
- timezone‑naive  
- ≥ Unix epoch  
- ≤ now + 1 second  
- interpreter timestamps strictly increase by +1 second

### **3.2 ID**
- starts with `"obs_"`  
- ≤ 64 chars  
- globally unique  
- interpreter IDs follow `obs_sys_000001`, …

### **3.3 Content**
- non‑empty  
- UTF‑8 encodable  
- ≤ 10,000 chars  
- interpreter content:  
  `Derived: {last_context_content} -> {input_content}`

### **3.4 Source**
Allowed: `user`, `memory`, `tool`, `environment`, `system`  
Interpreter always emits `system`.

---

## **4. Cross‑Field Provenance Rules (source → origin)**

- memory → {memory, system}  
- tool → tool  
- environment → {sensor, environment}  
- system → system  
- user → user  

---

## **5. ObservationStream Invariants**

### **5.1 Structure**
- `id: str`  
- `observations: list[Observation]`  
- non‑empty

### **5.2 Stream ID**
- starts with `"stream_"`  
- ≤ 64 chars  
- globally unique  
- interpreter IDs follow `stream_sys_000001`, …

### **5.3 Temporal Ordering**
- timestamps strictly increasing  
- no equality  
- no regression  

---

## **6. Subsystem 6 — Deterministic Reasoning Engine (Complete)**

Deterministic interpreter, deterministic multi‑step reasoning, deterministic trees, deterministic pruning, multi‑branch coherence, and full tree‑level determinism.

---

## **7. Subsystem 7 — Semantic–Epistemic Identity Layer (Complete)**

Semantic compression, provenance‑weighted semantics, epistemic profiles, unified identity hash, identity‑preserving transformations, cross‑tree identity convergence.

Subsystem 7 is a **closed semantic–epistemic identity substrate**.

---

## **8. Subsystem 8 — Temporal Identity Layer (Complete)**

Temporal anchor, continuity hash, drift, stability class, coherence hash, lineage hash, compression hash, temporal provenance hash.

Subsystem 8 is a **closed temporal identity substrate**.

---

## **9. Phase 9 — Emergent Agentic Behavior (Complete)**

Cross‑session identity, agentic continuity, self‑referential identity, multi‑tree lineage, deterministic memory objects, memory stability, memory chains, memory provenance.

---

## **10. Phase 10 — Agent Framework Layer (Complete)**

Ten deterministic agent surfaces:

1. agent_identity_hash  
2. agent_continuity_hash  
3. agent_memory_hash  
4. agent_behavior_hash  
5. agent_policy_hash  
6. agent_policy_continuity_hash  
7. agent_temporal_policy_hash  
8. agent_execution_anchor_hash  
9. agent_execution_lineage_hash  
10. agent_execution_provenance_hash  

---

## **11. Phase 11 — Deterministic Temporal Execution Loop (Complete)**

Nine temporal execution surfaces:

1. loop_identity  
2. step_anchor  
3. step_progression  
4. cycle_identity  
5. cycle_progression  
6. epoch_identity  
7. epoch_progression  
8. horizon_identity  
9. horizon_progression  

---

## **12. Phase 12 — Agentic Temporal Coherence (Complete)**

Two meta‑temporal surfaces:

1. agentic_temporal_coherence_hash  
2. agentic_temporal_coherence_progression_hash  

---

## **13. Phase 13 — Agentic Temporal Field (Complete)**

Field‑level invariants enabling reasoning about:

- temporal gradients  
- temporal curvature  
- horizon‑scale attractors  
- long‑range temporal structure  
- emergent temporal fields  

---

## **14. Phase 14 — Agentic Temporal Field Progression (In Progress)**  
### Completed Surfaces (14.1–14.20)

- 14.1 Temporal Gradient Surface  
- 14.2 Temporal Curvature Surface  
- 14.3 Temporal Attractor Surface  
- 14.4 Temporal Response Surface  
- 14.5 Temporal Reaction Surface  
- 14.6 Temporal Influence Surface  
- 14.7 Temporal Regulation Surface  
- 14.8 Temporal Stabilization Surface  
- 14.9 Temporal Homeostasis Surface  
- 14.10 Temporal Equilibrium Surface  
- 14.11 Harmonic‑Interference Synthesis Surface  
- 14.12 Diffraction Surface  
- 14.13 Diffraction‑Interference Synthesis Surface  
- 14.14 Diffraction‑Harmonic Synthesis Surface  
- 14.15 Harmonic‑Diffraction Synthesis Surface  
- 14.16 Interference‑Harmonic‑Diffraction Synthesis Surface  
- 14.17 Harmonic‑Interference‑Diffraction Synthesis Surface  
- 14.18 Full Synthesis Lattice Surface  
- 14.19 Lattice Coherence Surface  
- 14.20 Lattice Stability Surface  

### Phase 14 Summary  
Phase 14 constructs a **complete temporal‑field lattice**, integrating gradient, curvature, attractor, harmonic, interference, diffraction, and all synthesis surfaces into a coherent, stable temporal‑field geometry.

---

## **15. Test Suite Status**

- **173 tests passing**  
- All invariants sealed through Phase 14.20  
- Temporal‑field lattice stable and coherent  

---

## **16. Development Principles**

- strict TDD  
- minimal deterministic patches  
- semantic nucleus preservation  
- provenance integrity  
- temporal determinism  
- architectural hygiene  

---

## **17. Roadmap**

- Phase 14.21 — Temporal Field Lattice Stability Progression  
- Phase 15 — Temporal Field Autonomy  
- Phase 16 — Agentic Temporal Self‑Regulation  

TESLA’s long‑term trajectory is to serve as a **civilizational infrastructure for trust, provenance, and continuity**.

---