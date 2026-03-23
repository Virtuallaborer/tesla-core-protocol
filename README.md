# **README.md (Enhanced Project Overview)**

# 🔷 TESLA Core Protocol  
*A truth‑preserving substrate for agentic systems*

The TESLA Core Protocol is a foundational architecture for building **provenance‑anchored**, **deterministic**, and **truth‑preserving** agentic systems. It defines strict invariants for observations, provenance, temporal ordering, and source adjacency, forming a substrate that later layers (orchestration and emergence) can rely on without contradiction.

This repository contains the **reference implementation** of the protocol in Python using **Pydantic v2**, along with a comprehensive test suite enforcing all invariants through strict TDD.

---

## 🚀 Vision

Modern AI systems lack **provenance**, **determinism**, and **structural guarantees**.  
The TESLA Core Protocol solves this by defining:

- A **unified observation model**  
- A **cryptographically meaningful provenance layer**  
- A **temporal and causal ordering system**  
- A **source‑adjacency lattice** that prevents impossible transitions  
- A **test‑driven, invariant‑driven development cycle**  

This creates a substrate where higher‑order agentic behavior can emerge safely and predictably.

---

# 🔷 3‑6‑9 DESIGN PHILOSOPHY

TESLA is built using a **3‑phase progression**:

### **3 → Foundations**  
We construct the primitive structures and invariants:
- Observation  
- Provenance  
- Temporal invariants  
- Structural invariants  
- Semantic invariants  
- Adjacency lattice  

### **6 → Orchestration**  
Subsystems begin coordinating:
- Multi‑stream coherence  
- Semantic adjacency  
- Causal windows  
- Memory consolidation  
- Tool orchestration  

### **9 → Emergence**  
Higher‑order behavior emerges from the substrate:
- Agentic reasoning  
- Self‑consistent world modeling  
- Long‑horizon coherence  
- Autonomous workflows  

We are currently completing the **3‑phase**.

---

# 🔷 Current Project State (March 2026)

The protocol currently defines **three Pydantic v2 models**:

- `Provenance`  
- `Observation`  
- `ObservationStream`

The test suite contains **42 tests**, all passing, enforcing:

---

## ✔ Provenance Invariants

- `hash`: lowercase hex, 32–256 chars  
- `origin`: lowercase `[a-z0-9_]`  
- `confidence`: 0.0–1.0 inclusive  

---

## ✔ Observation Invariants

- strict `datetime`  
- timezone‑naive  
- ≥ Unix epoch  
- ≤ now + 1s drift  
- globally unique ID (`obs_…`)  
- UTF‑8 safe content  
- ≤ 10,000 chars  
- source ∈ {user, memory, tool, environment, system}

---

## ✔ Cross‑Field Rules (source → origin)

- memory → {memory, system}  
- tool → tool  
- environment → {sensor, environment}  
- system → system  
- user → user  

---

## ✔ Subsystem 3 — Temporal Ordering (Complete)

- timestamps strictly increasing  
- no equality  
- no regression  

---

## ✔ Subsystem 4 — Source Adjacency Lattice (Complete)

All **15 forbidden transitions** are enforced:

```
system → user
environment → memory
user → tool
tool → memory
system → memory
memory → system
tool → system
environment → system
user → system
memory → user
tool → user
memory → tool
memory → environment
system → environment
tool → environment
```

Subsystem 4 is now **fully closed** and structurally complete.

---

# 🔷 TDD Workflow (Strict)

All development follows a strict invariant‑driven TDD cycle:

1. Propose the next invariant  
2. Write the failing test  
3. Run pytest  
4. Implement the minimal fix  
5. Run pytest again  
6. Repeat  

No invariants or fields may be added without a failing test.

---

# 🔷 Repository Structure

```
tesla-core-protocol/
│
├── models/
│   ├── observation.py
│   ├── provenance.py
│   └── stream.py
│
├── tests/
│   ├── test_observation.py
│   ├── test_provenance.py
│   └── test_stream.py
│
├── README.md
└── TESLA_PROTOCOL.md
```

---

# 🔷 Roadmap

### **Phase 3 (Foundations) — Current**
- Subsystem 3: Temporal Ordering ✔  
- Subsystem 4: Source Adjacency ✔  
- Subsystem 5: Semantic Adjacency (next)  
- Subsystem 6: Stream‑Level Provenance Coherence  
- Subsystem 7: Causal Windows  

### **Phase 6 (Orchestration)**
- Multi‑stream integration  
- Memory consolidation  
- Tool orchestration  
- Context propagation  

### **Phase 9 (Emergence)**
- Agentic reasoning  
- Long‑horizon coherence  
- Autonomous workflows  

---

# 🔷 Contributing

Contributions must follow the **strict TDD workflow** and respect the **3‑6‑9 design philosophy**.  
All invariants must be introduced through failing tests.

---

# 🔷 License

MIT License (or your preferred license).
