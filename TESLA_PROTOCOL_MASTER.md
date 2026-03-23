Patrick, this is exactly the right moment to seal the work, freeze the ontology, and prepare a clean launchpad for the next session. You’ve just completed Subsystem 4 — the entire adjacency lattice — and that deserves a pristine, authoritative `.md` file you can drop into any new chat to restore the full state of the TESLA Core Protocol.

Below is the **complete, consolidated, up‑to‑date TESLA PROTOCOL.md**, reflecting everything through **Invariant 4.15** and **42 passing tests**.  
It’s clean, self‑contained, and ready for copy‑paste into your next session.

---

# **TESLA_PROTOCOL.md (Authoritative, March 2026)**

# 🔷 **TESLA Core Protocol — Authoritative Project State**  
*Reflecting progress through Invariant 4.15 and 42 passing tests*

We are continuing work on the TESLA Core Protocol.

This document is the **single source of truth** for the project’s current state, invariants, models, and TDD workflow.  
Paste this into any new chat session to restore full continuity.

---

# **1. TESLA 3‑6‑9 DESIGN PHILOSOPHY**

The TESLA Core Protocol is built using a **3‑6‑9 progression**:

### **3 → Foundations**  
Primitive truth‑preserving structures:  
- Observation  
- Provenance  
- Cross‑field invariants  
- Temporal invariants  
- Structural invariants  
- Semantic invariants  

### **6 → Orchestration**  
Subsystem activation, coordination, and multi‑stream coherence.

### **9 → Emergence**  
Agentic behavior, semantic adjacency, and higher‑order invariants.

We are currently in the **3‑phase**, completing the foundational substrate.

All future work must align with this trajectory.

---

# **2. CURRENT MODELS (Pydantic v2)**

The project contains three models:

- **Provenance**  
- **Observation**  
- **ObservationStream**

All invariants below are enforced by the passing test suite.

---

# **3. PROVENANCE INVARIANTS**

### `hash`
- non‑empty  
- lowercase hex  
- length 32–256  

### `origin`
- lowercase  
- non‑empty  
- characters: `[a-z0-9_]`  

### `confidence`
- float between **0.0 and 1.0 inclusive**

---

# **4. OBSERVATION INVARIANTS**

### `timestamp`
- strict `datetime`  
- timezone‑naive  
- ≥ Unix epoch  
- ≤ now + 1 second (drift tolerance)

### `id`
- starts with `"obs_"`  
- suffix: lowercase letters, digits, underscores  
- ≤ 64 characters  
- globally unique (instance‑idempotent)

### `content`
- non‑empty  
- UTF‑8 encodable  
- valid Unicode  
- ≤ 10,000 characters  

### `source`
Allowed values:  
`user`, `memory`, `tool`, `environment`, `system`

---

# **5. CROSS‑FIELD PROVENANCE RULES (source → origin)**

- memory → {memory, system}  
- tool → tool  
- environment → {sensor, environment}  
- system → system  
- user → user  

These are fully enforced.

---

# **6. OBSERVATIONSTREAM INVARIANTS**

### Structure
- `id: str`  
- `observations: list[Observation]`

---

# **7. SUBSYSTEM 3 — CONTEXTUAL INTEGRATION (Complete)**

Stream‑level timestamp rules:

1. timestamps strictly increasing  
2. no equality  
3. no regression  

All enforced via model‑level validator.

---

# **8. SUBSYSTEM 4 — SOURCE ADJACENCY INVARIANTS (Complete)**

Subsystem 4 enforces **pairwise source‑transition rules** between consecutive observations.

All 15 invariants are implemented and passing.

### **Forbidden Source Transitions**

| Invariant | Transition | Status |
|----------|------------|--------|
| 4.1 | system → user | ❌ |
| 4.2 | environment → memory | ❌ |
| 4.3 | user → tool | ❌ |
| 4.4 | tool → memory | ❌ |
| 4.5 | system → memory | ❌ |
| 4.6 | memory → system | ❌ |
| 4.7 | tool → system | ❌ |
| 4.8 | environment → system | ❌ |
| 4.9 | user → system | ❌ |
| 4.10 | memory → user | ❌ |
| 4.11 | tool → user | ❌ |
| 4.12 | memory → tool | ❌ |
| 4.13 | memory → environment | ❌ |
| 4.14 | system → environment | ❌ |
| 4.15 | tool → environment | ❌ |

### **Subsystem 4 Summary**
- All internal → external transitions are forbidden  
- All external → system transitions are forbidden  
- Memory is a pure sink  
- System is an internal root  
- Environment is an external root  
- The adjacency lattice is now fully closed and contradiction‑free  

Subsystem 4 is **complete**.

---

# **9. TEST SUITE STATUS**

### Total tests: **42**  
### Passing: **42**  
### Failing: **0**

Covers:
- Provenance invariants  
- Observation invariants  
- Cross‑field rules  
- Stream‑level timestamp rules  
- All 15 adjacency invariants  

The suite is stable and authoritative.

---

# **10. STRICT TDD WORKFLOW**

For every new invariant:

1. You propose the next invariant  
2. You write the failing test  
3. I run pytest  
4. You provide the minimal implementation  
5. I run pytest again  
6. Repeat  

You must NOT:
- rewrite existing tests unless explicitly asked  
- rewrite existing models unless required by failing tests  
- assume timestamps can be strings  
- assume new provenance origins  
- generate nested tests or duplicate test names  
- break the 3‑6‑9 progression  

---

# **11. NEXT PHASE**

Subsystem 4 is complete.  
The next subsystem to activate will be **Subsystem 5**, unless the 3‑phase requires additional foundational invariants.

This document is the authoritative state for beginning the next session.
