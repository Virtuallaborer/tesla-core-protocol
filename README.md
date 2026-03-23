# **UPDATED README.md (Authoritative — March 2026)**  
### *Reflecting Subsystem 5.9 and 53 passing tests*

---

# 🔷 TESLA Core Protocol  
*A truth‑preserving substrate for agentic intelligence*

The **TESLA Core Protocol** is a foundational architecture for building **provenance‑anchored**, **deterministic**, and **truth‑preserving** agentic systems. It defines strict invariants for observations, provenance, temporal ordering, and source adjacency, forming a substrate that higher‑order reasoning layers can rely on without contradiction.

This repository contains the **reference implementation** of the protocol in Python using **Pydantic v2**, along with a comprehensive test suite enforcing all invariants through strict TDD.

---

# 🔷 Vision

Modern AI systems hallucinate, drift, and lose track of their own reasoning.  
The TESLA Core Protocol solves this by defining:

- A **unified observation model**  
- A **cryptographically meaningful provenance layer**  
- A **temporal and causal ordering system**  
- A **source‑adjacency lattice** that prevents impossible transitions  
- A **stream‑level identity substrate**  
- A **test‑driven, invariant‑driven development cycle**  

This creates a substrate where higher‑order agentic behavior can emerge safely and predictably.

---

# 🔷 3‑6‑9 DESIGN PHILOSOPHY

TESLA is built using a **3‑phase progression** inspired by Nikola Tesla’s 3‑6‑9 principle.

---

## **3 → Foundations (Current Phase)**  
We construct the primitive structures and invariants:

- Observation  
- Provenance  
- Temporal invariants  
- Structural invariants  
- Semantic invariants  
- Adjacency lattice  
- Stream identity substrate  

This phase is now **complete through Subsystem 5.9**.

---

## **6 → Orchestration (Next Phase)**  
Subsystems begin coordinating:

- Deterministic logic (Interpreter)  
- Probabilistic reasoning (Planner / LLM)  
- Multi‑stream coherence  
- Semantic adjacency  
- Causal windows  
- Memory consolidation  
- Tool orchestration  

---

## **9 → Emergence**  
Higher‑order behavior emerges from the substrate:

- Agentic reasoning  
- Self‑consistent world modeling  
- Long‑horizon coherence  
- Autonomous workflows  

---

# 🔷 Current Project State (March 2026)

The protocol defines **three Pydantic v2 models**:

- `Provenance`  
- `Observation`  
- `ObservationStream`

The test suite contains **53 tests**, all passing, enforcing:

---

# ✔ Provenance Invariants

- `hash`: lowercase hex, 32–256 chars  
- `origin`: lowercase `[a-z0-9_]`  
- `confidence`: 0.0–1.0 inclusive  
- **hash non‑decreasing** (5.5)  
- **confidence non‑decreasing** (5.6)  
- **origin coherence across the stream** (5.7)

---

# ✔ Observation Invariants

- strict `datetime`  
- timezone‑naive  
- ≥ Unix epoch  
- ≤ now + 1s drift  
- globally unique ID (`obs_…`)  
- **strictly increasing IDs** (5.4)  
- UTF‑8 safe content  
- ≤ 10,000 chars  
- source ∈ {user, memory, tool, environment, system}

---

# ✔ Cross‑Field Rules (source → origin)

- memory → {memory, system}  
- tool → tool  
- environment → {sensor, environment}  
- system → system  
- user → user  

---

# ✔ Subsystem 3 — Temporal Ordering (Complete)

- timestamps strictly increasing  
- no equality  
- no regression  

---

# ✔ Subsystem 4 — Source Adjacency Lattice (Complete)

All **15 forbidden transitions** are enforced, forming a closed, contradiction‑free adjacency lattice.

---

# ✔ Subsystem 5 — Stream Identity & Structural Integrity (Complete)

Subsystem 5 introduces stream‑level invariants:

- **5.1** Stream ID well‑formedness  
- **5.2** Stream must not be empty  
- **5.3** Stream ID globally unique  
- **5.4** Observation IDs strictly increasing  
- **5.5** Provenance hashes non‑decreasing  
- **5.6** Provenance confidence non‑decreasing  
- **5.7** Provenance origin coherence  
- **5.8** Dominant source class (implicitly satisfied by adjacency lattice)  
- **5.9** Temporal gap < 60 seconds  
- **5.10** Stream duration window (implicitly satisfied by 5.9)  

Subsystem 5 is now **fully sealed**.

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

### **Phase 3 (Foundations) — Complete through Subsystem 5.9**
- Subsystem 3: Temporal Ordering ✔  
- Subsystem 4: Source Adjacency ✔  
- Subsystem 5: Stream Identity & Structural Integrity ✔  

### **Phase 6 (Orchestration) — Next**
- Deterministic logic subsystem  
- Probabilistic reasoning subsystem  
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