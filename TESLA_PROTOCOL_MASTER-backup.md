# ✅ **TESLA_PROTOCOL.md (Authoritative — March 2026)**  
### *Reflecting progress through Subsystem 6.6.F and 85 passing tests*

---

# **1. TESLA 3‑6‑9 DESIGN PHILOSOPHY**

The TESLA Core Protocol is built using a **3‑6‑9 progression**, inspired by Nikola Tesla’s principle that 3, 6, and 9 encode the structure of natural order.

### **3 → Foundations**  
Irreducible truth‑preserving primitives:

- **Observation**
- **Provenance**
- **Cross‑field invariants**
- **Temporal invariants**
- **Structural invariants**
- **Semantic invariants**

### **6 → Orchestration**  
Dual subsystem pairs that coordinate perception, reasoning, and action.

### **9 → Emergence**  
Self‑monitoring, self‑correction, memory formation, skill acquisition, and bounded autonomy.

We are now deep into the **6‑phase**, where deterministic reasoning emerges.

---

# **2. CURRENT MODELS (Pydantic v2)**

The protocol defines four core models:

- **Provenance**
- **Observation**
- **ObservationStream**
- **ReasoningTree** (introduced in Subsystem 6.3)

All invariants listed below are enforced by the passing test suite.

---

# **3. PROVENANCE INVARIANTS**

### `hash`

- **non‑empty**
- **lowercase hex**
- **length 32–256**
- **non‑decreasing within a stream** (Subsystem 5.5)
- **Interpreter‑generated hashes are deterministic SHA‑256** (Subsystem 6.1.3)
- **Interpreter‑generated hashes are monotonic via last‑hash carryover** (Subsystem 6.1.4)
- **Chain‑level aggregated hash = SHA256(h₁ + h₂ + … + hₙ)** (Subsystem 6.2.4)

### `origin`

- **lowercase**
- **non‑empty**
- characters: `[a-z0-9_]`
- must match allowed source→origin mapping (Section 5)
- **must be coherent across the entire stream** (Subsystem 5.7)

### `confidence`

- float between **0.0 and 1.0 inclusive**
- **non‑decreasing within a stream** (Subsystem 5.6)
- **Interpreter confidence = 1 / (1 + counter)** (Subsystem 6.1.6)
- **Chain‑level confidence = product of all step confidences** (Subsystem 6.2.5)

---

# **4. OBSERVATION INVARIANTS**

### `timestamp`

- strict `datetime`
- timezone‑naive
- ≥ Unix epoch
- ≤ now + 1 second
- **Interpreter timestamps strictly increase by +1 second per inference** (Subsystem 6.1.2)

### `id`

- starts with `"obs_"`
- suffix: lowercase letters, digits, underscores
- ≤ 64 characters
- globally unique
- **Interpreter IDs follow `obs_sys_000001`, `obs_sys_000002`, …** (Subsystem 6.1.1)

### `content`

- non‑empty
- UTF‑8 encodable
- valid Unicode
- ≤ 10,000 characters
- **Interpreter content is deterministically derived:**

  ```text
  Derived: {last_context_content} -> {input_content}
  ```

  (Subsystem 6.1.5)

### `source`

Allowed values:

- `user`
- `memory`
- `tool`
- `environment`
- `system`

Interpreter always emits:

- `source = "system"`

---

# **5. CROSS‑FIELD PROVENANCE RULES (source → origin)**

These rules ensure that provenance origin is consistent with the Observation’s source:

- **memory → {memory, system}**
- **tool → tool**
- **environment → {sensor, environment}**
- **system → system**
- **user → user**

All enforced.

---

# **6. OBSERVATIONSTREAM INVARIANTS**

### Structure

- `id: str`
- `observations: list[Observation]`

### Stream ID

- must start with `"stream_"`
- suffix: lowercase letters, digits, underscores
- ≤ 64 characters
- **Interpreter stream IDs follow `stream_sys_000001`, `stream_sys_000002`, …** (Subsystem 6.1.1)

---

# **7. SUBSYSTEM 3 — TEMPORAL INTEGRATION (Complete)**

Stream‑level timestamp rules:

1. **timestamps strictly increasing**
2. **no equality**
3. **no regression**

Fully enforced.

---

# **8. SUBSYSTEM 4 — SOURCE ADJACENCY INVARIANTS (Complete)**

Subsystem 4 enforces **pairwise source‑transition rules** between consecutive observations.

Subsystem 4 is **complete**.

---

# **9. SUBSYSTEM 5 — STREAM IDENTITY & STRUCTURAL INTEGRITY (Complete)**

Subsystem 5 introduces invariants that ensure:

- **stream‑level identity coherence**
- **provenance monotonicity**
- **temporal continuity**
- **structural integrity**

Subsystem 5 is **complete**.

---

# **10. SUBSYSTEM 6 — DETERMINISTIC INTERPRETER**

Subsystem 6 introduces the **Interpreter**, the first reasoning engine in TESLA.

---

## **6.1 — Deterministic Logic Engine (Complete)**

### **6.1.1 — Deterministic ID Strategy**

Interpreter emits:

- `stream_sys_000001`, `stream_sys_000002`, …
- `obs_sys_000001`, `obs_sys_000002`, …

### **6.1.2 — Deterministic Timestamp Strategy**

Interpreter timestamps:

```text
last_context_timestamp + counter seconds
```

### **6.1.3 — Deterministic Provenance Hash Strategy**

Hash input:

```text
{context.id}|{last_obs.id}|{content}|{counter}
```

- Hash algorithm: **SHA‑256**
- Output: **64‑char lowercase hex**

### **6.1.4 — Monotonic Provenance Hash Enforcement**

If new hash < last hash → use last hash instead.

### **6.1.5 — Deterministic Content Derivation**

Interpreter content:

```text
Derived: {last_context_content} -> {input_content}
```

### **6.1.6 — Deterministic Confidence Strategy**

Confidence:

```text
1 / (1 + counter)
```

---

## **6.2 — Deterministic Multi‑Step Reasoning (Complete)**

Subsystem 6.2 extends the Interpreter into a **deterministic multi‑step reasoning engine**.

- **6.2.1 — Deterministic Chaining**
- **6.2.2 — Deterministic Recursive Thought Chains**
- **6.2.3 — Deterministic Depth‑Limited Reasoning**
- **6.2.4 — Deterministic Chain Provenance Aggregation**
- **6.2.5 — Deterministic Chain Confidence Aggregation**
- **6.2.6 — Deterministic Chain Termination Conditions**

All complete and enforced.

---

## **6.3 — Deterministic Reasoning Trees**

Subsystem 6.3 extends the Interpreter from linear deterministic chains into **deterministic branching reasoning trees**.  
These trees preserve all invariants from Subsystems 6.1 and 6.2 while introducing structured multi‑path cognition, deterministic selection, and introspective trace extraction.

- **6.3.0 — Deterministic Two‑Branch Reasoning Tree (Complete)**
- **6.3.1 — Deterministic Branch Depth Control (Complete)**
- **6.3.2 — Deterministic Branch Internal Structure (Complete)**
- **6.3.3 — Deterministic Multi‑Branch Generalization (Complete)**
- **6.3.4 — Deterministic Branch Selection (Complete)**
- **6.3.5 — Deterministic Selection Justification (Complete)**
- **6.3.6 — Deterministic Branch Scoring (Complete)**
- **6.3.7 — Deterministic Branch Ranking (Complete)**
- **6.3.8 — Deterministic Branch Trace Extraction (Complete)**
- **6.3.9 — Deterministic Branch Metadata (Complete)**

All invariants and behaviors from these subsystems are fully implemented and enforced by the test suite.

### **6.3.10 — Deterministic Tree Summary (Complete)**

The Interpreter emits a compact, deterministic summary of the entire reasoning tree.

**Summary structure:**

```python
summary = {
    "root_context_id": str,
    "num_branches": int,
    "branch_keys": list[str],
    "selected_branch": str,
    "selected_branch_score": int,
    "selected_branch_depth": int,
    "selected_branch_num_observations": int,
    "tree_provenance_hash": str,
    "tree_provenance_confidence": float,
}
```

**Deterministic properties:**

- All fields are computed **after** branch selection, scoring, ranking, and metadata generation.
- Summary is **purely descriptive** — it introduces no new behavior.
- Summary is **fully reproducible** from:
  - `branches`
  - `branch_scores`
  - `branch_metadata`
  - `selected_branch`
  - `provenance`

**Purpose:**

- compact, machine‑verifiable representation of the reasoning tree  
- stable interface for downstream subsystems (6.4+, 9.x)  
- deterministic snapshot of the Interpreter’s cognitive state  

Subsystem 6.3 is now fully complete through **6.3.10**.

---

## **6.4 — Deterministic Branch Pruning (Complete)**

Subsystem 6.4 introduces **deterministic pruning** of reasoning branches, allowing the Interpreter to retain only the most relevant branches while preserving all invariants from 6.1–6.3.

### **6.4.0 — Deterministic Rank‑Based Pruning (Complete)**

The Interpreter accepts:

```python
prune_below_rank: int | None
```

**Behavior:**

- If `prune_below_rank is None` → no pruning is applied.
- If `prune_below_rank = N` → only the **top N branches** (by deterministic ranking) are retained.

Pruning is based on existing **branch ranking** (6.3.7), computed from deterministic branch scores (6.3.6) derived from final provenance hashes.

After pruning:

- `branches` contains only the top N branches.
- `branch_scores` contains only the top N branches.
- `branch_ranking` is truncated to the top N entries.
- `branch_metadata` is truncated to the top N entries.
- If the previously selected branch was pruned, the **top‑ranked branch** becomes the new `selected_branch`.

### **6.4.1 — Post‑Pruning Invariants (Complete)**

After pruning, the Interpreter **recomputes**:

- **Selected branch trace** — using the (possibly updated) `selected_branch`.
- **Tree‑level provenance**:
  - Hash recomputed from final observations of retained branches.
  - Confidence recomputed as the product of retained branches’ final confidences.
- **Tree summary** (6.3.10):
  - `num_branches` reflects the pruned count.
  - `branch_keys` lists only retained branches.
  - `selected_branch` and `selected_branch_score` are consistent with the pruned state.
  - `tree_provenance_hash` and `tree_provenance_confidence` match the recomputed tree‑level provenance.

Pruning is:

- **Deterministic** — pure function of already‑computed scores and ranking.
- **Reproducible** — no randomness or external state.
- **Invariant‑preserving** — all structural and provenance invariants remain valid after pruning.

Subsystem 6.4 is **complete**.

---

## **6.5 — Multi‑Branch Coherence Invariants (Complete)**

Subsystem 6.5 defines the coherence rules that govern the structure and internal consistency of a `ReasoningTree` produced by the `DeterministicInterpreter`.  
These invariants ensure that all branches, timestamps, provenance signals, and selection traces remain aligned with the root context and with each other.

Through test‑driven validation, all invariants in this subsystem were confirmed to be **structurally guaranteed by the existing architecture**.  
No additional validators or interpreter modifications were required.  
The invariants are now explicitly codified and enforced through the test suite.

Subsystem 6.5 is **complete**.

---

## **6.6 — Tree‑Level Determinism and Identity**

Subsystem 6.6 introduces invariants governing the identity, reproducibility, and cross‑run stability of `ReasoningTree` artifacts.  
While Subsystem 6.5 focused on *intra‑tree coherence*, Subsystem 6.6 elevates the guarantees to the *tree level*, ensuring that reasoning artifacts are stable, comparable, and suitable for provenance anchoring and caching.

---

### **6.6.A — Deterministic ReasoningTree Identity**

**Invariant:**  
A `ReasoningTree` must expose a deterministic `id` that is a pure function of its structurally stable inputs.  
For identical interpreter inputs, the resulting `ReasoningTree` must have an identical `id` across runs, sessions, and environments.

**Rationale:**  
Tree‑level identity is foundational for:

- reproducibility
- caching and deduplication
- provenance anchoring
- multi‑agent coordination
- cross‑session continuity
- deterministic debugging

Interpreter‑generated IDs (e.g., `tree_sys_000001`) are inherently non‑deterministic because they depend on global counters and runtime state.  
Subsystem 6.6.A replaces this with a deterministic identity derived solely from stable structural properties of the tree.

**Identity function:**

```text
sha256(
    root_context.id
    + number_of_branches
    + sorted_branch_keys
)
```

Final tree identifier:

```text
tree_<first_16_hex_chars_of_hash>
```

This ensures:

- identical inputs → identical tree structure → identical tree ID
- no dependence on interpreter counters
- no dependence on provenance hashes or selection metadata
- stability across runs and environments

**Status:**  
Implemented via a `model_validator(mode="after")` inside `ReasoningTree`.  
The validator overrides any interpreter‑provided ID, ensuring the tree owns its identity.

**Test coverage:**  
`test_reasoning_tree_id_is_deterministic`

---

### **6.6.B — Structural Equivalence for Identical Inputs**

**Invariant:**  
Two *fresh* `DeterministicInterpreter` instances, when given identical inputs, must produce `ReasoningTree` artifacts that are structurally identical.  
This includes:

- identical deterministic tree ID
- identical branch keys
- identical selected branch
- identical selection justification
- identical summary
- identical branch metadata
- identical branch scores and rankings
- identical selected branch trace

**Rationale:**  
Subsystem 6.6.A ensures that a `ReasoningTree` has a deterministic identity.  
Subsystem 6.6.B extends this guarantee to the *entire structure* of the tree, ensuring that reasoning artifacts are reproducible across:

- sessions
- environments
- interpreter instances
- distributed systems

This is essential for:

- caching
- provenance anchoring
- multi‑agent consistency
- deterministic debugging
- long‑term reproducibility

**Scope clarification:**  
The TESLA Core Protocol enforces global uniqueness for `Observation` and `ObservationStream` IDs.  
Therefore, structural equivalence is defined in terms of **fresh interpreter state** and **fresh ID registries**.  
This ensures that deterministic behavior is measured independently of global uniqueness constraints.

**Status:**  
Guaranteed by construction when:

- each tree is produced by a fresh `DeterministicInterpreter`
- ID registries (`Observation._used_ids`, `ObservationStream._used_stream_ids`) are reset between builds
- the deterministic `ReasoningTree` identity function (6.6.A) is applied
- interpreter internal counters (`_counter`, `_last_hash`) begin at their initial state

**Test coverage:**  
`test_reasoning_tree_structural_equivalence_for_identical_inputs`

---

### **6.6.C — Semantic Monotonicity of Branches**

**Invariant:**  
Every branch in a `ReasoningTree` must be a **semantic continuation** of the root context.  
A branch may diverge, elaborate, reinterpret, or extend the meaning of the root, but it may **not contradict** it.

**Definition:**  
A branch is semantically monotonic if its final observation:

- preserves the core meaning of the root context
- does not introduce a direct negation of the root’s assertions
- does not reset, invert, or invalidate the root’s content
- remains within the semantic frame established by the root

This ensures that all branches represent **valid hypothetical continuations** of the same initial state.

**Rationale:**  
Subsystems 6.6.A and 6.6.B establish deterministic identity and deterministic structure.  
Subsystem 6.6.C extends determinism into the semantic domain, ensuring that reasoning artifacts remain coherent and truth‑preserving.

This invariant prevents the interpreter from generating branches that:

- contradict the user’s input
- undermine the root context
- introduce semantic resets
- violate the continuity of meaning

**Enforcement:**  
The interpreter enforces a simple, deterministic guardrail: when a branch’s content would directly negate the root context, it is rewritten into a monotonic continuation, preserving semantic alignment with the root.

**Test coverage:**  
`test_reasoning_tree_rejects_semantically_contradictory_branch`

**Status:**  
Guaranteed by construction.

---

### **6.6.D — Cross‑Branch Semantic Convergence**

**Invariant:**  
All branches in a `ReasoningTree` must share a **semantic nucleus** with the root context.  
Branches may elaborate, extend, or reinterpret the root’s meaning, but they may not drift into unrelated semantic domains.

**Definition:**  
A branch satisfies semantic convergence if its final observation:

- contains at least one keyword from the root context
- preserves the conceptual frame established by the root
- remains anchored to the same semantic domain
- does not introduce unrelated or orthogonal topics

This ensures that all branches represent **coherent variations** of the same underlying meaning.

**Rationale:**  
Subsystem 6.6.C prevents contradictions.  
Subsystem 6.6.D prevents semantic drift.

Together, they ensure that a `ReasoningTree` is not merely structurally deterministic, but also **semantically coherent** across all branches.

**Enforcement:**  
The deterministic transformation applied by the interpreter:

```text
Derived: {root_content} -> {input_content}
```

inherently preserves root‑context keywords, ensuring convergence **by construction**.

**Test coverage:**  
`test_reasoning_tree_branches_share_semantic_nucleus`

**Status:**  
Guaranteed by construction.

---

### **6.6.E — Selection‑Trace Coherence**

**Invariant:**  
The `selected_branch_trace` of a `ReasoningTree` must exactly match the sequence of observations along the selected branch.

**Definition:**  
Given:

- `selected_branch` key
- `branches[selected_branch]` (either a single `ObservationStream` or a list of them)

The Interpreter must ensure that:

- `selected_branch_trace` is the ordered list of all observations along that branch
- the IDs and ordering in `selected_branch_trace` are identical to those in the branch itself

**Rationale:**  
This invariant makes the tree **self‑describing**:

- the selected branch can be reconstructed from the trace
- the trace is a faithful reflection of the actual branch
- downstream systems can trust the trace as a canonical representation of the chosen reasoning path

**Enforcement:**  
The interpreter constructs `selected_branch_trace` directly from the selected branch’s observations, in order.

**Test coverage:**  
`test_reasoning_tree_selected_branch_trace_matches_branch`

**Status:**  
Guaranteed by construction.

---

### **6.6.F — Tree‑Level Coherence Invariant**

**Invariant:**  
A `ReasoningTree` must be internally coherent as a whole.  
Its identity, structure, semantics, provenance, selection, justification, summary, and trace must all align to form a single, deterministic reasoning artifact.

This invariant is satisfied when all of the following hold simultaneously:

- **6.6.A — Deterministic identity:**  
  The tree’s `id` is a pure function of its structure.
- **6.6.B — Structural equivalence:**  
  Identical inputs yield structurally identical trees across fresh interpreters.
- **6.6.C — Semantic monotonicity:**  
  No branch contradicts the root context.
- **6.6.D — Semantic convergence:**  
  All branches share a semantic nucleus with the root.
- **6.6.E — Selection‑trace coherence:**  
  `selected_branch_trace` exactly matches the observations along the selected branch.

**Rationale:**  
Subsystem 6.6 is not a collection of independent guarantees; it is a **coherence lattice**.  
When A–E all hold, a `ReasoningTree` becomes:

- **structurally deterministic**
- **semantically consistent**
- **self‑describing**
- **reproducible across runs and interpreters**

This is the minimal set of conditions under which a reasoning artifact can be treated as **truth‑preserving** within the TESLA Core Protocol.

**Status:**  
Guaranteed by construction as a direct consequence of 6.6.A–E and their associated tests.

---

# **11. TEST SUITE STATUS**

- **Total tests:** 85  
- **Passing:** 85  
- **Failing:** 0  

Subsystems complete:

- **6.1 — Deterministic Logic Engine**
- **6.2 — Deterministic Multi‑Step Reasoning**
- **6.3.0 → 6.3.10 — Deterministic Reasoning Trees**
- **6.4 — Deterministic Branch Pruning**
- **6.5 — Multi‑Branch Coherence Invariants**
- **6.6.A → 6.6.F — Tree‑Level Determinism and Identity**

The suite is **stable and authoritative**.

---

# **12. STRICT TDD WORKFLOW**

(Section unchanged; preserved from previous version.)

- Introduce **one invariant at a time**.
- Write **one failing test** that encodes the invariant.
- Confirm the test fails for the right reason.
- Apply the **minimal change** to satisfy the invariant.
- Re‑run the **full test suite**.
- Only then update `TESLA_PROTOCOL.md` to reflect the new truth.

---

# SUBSYSTEM 6.7**

The next subsystem will introduce:

- provenance‑anchored semantic coherence
- explicit linkage between tree‑level semantics and provenance chains
- preparation for emergence‑level subsystems in the **9‑phase**

Subsystem 6.7 will bridge:

- the **deterministic reasoning substrate** (Subsystems 6.1–6.6)  
and  
- the **Truth Preservation Project’s provenance‑anchored guarantees**.

6.7 — Provenance‑Anchored Semantic Coherence
6.7.0 — Deterministic Semantic Divergence & Provenance Coupling
Invariant:  
Branches in a ReasoningTree must exhibit deterministic semantic divergence, and this divergence must be reflected in their final provenance hashes.

Definition:  
For any two branches A and B in the same tree:

If A.final_content != B.final_content  
then
A.final_provenance.hash != B.final_provenance.hash

Rationale:  
Subsystems 6.6.C and 6.6.D ensure semantic monotonicity and convergence.
Subsystem 6.7 extends this by requiring that semantic differences produce cryptographic differences, binding meaning to provenance.

Implementation:  
Branch content is deterministically varied using the branch index:

Code
content + " [branch XXXX]"
Because provenance hashing incorporates content, semantic divergence produces deterministic provenance divergence.

Status:  
Enforced by test:
test_reasoning_tree_provenance_reflects_semantic_divergence_between_branches

# TESLA Core Protocol  
### Deterministic, Provenance‑Anchored Reasoning Substrate  
### Updated Through Subsystem 6.7.6  
---

## 1. Overview

The TESLA Core Protocol defines a deterministic, provenance‑anchored reasoning substrate built on three primitives:

- **Observation** — atomic, timestamped, provenance‑bearing unit  
- **ObservationStream** — ordered sequence of Observations  
- **ReasoningTree** — multi‑branch deterministic reasoning structure  

The protocol evolves through invariant‑driven development.  
Each subsystem introduces new guarantees without violating previously sealed invariants.

---

## 2. Primitives

### 2.1 Observation
- Unique ID  
- Timestamp  
- Source (`user` or `system`)  
- Content (immutable semantic payload)  
- Provenance:
  - `hash` — deterministic content‑anchored hash  
  - `origin` — source of the information  
  - `confidence` — multiplicative certainty metric  

### 2.2 ObservationStream
- Unique ID  
- Ordered list of Observations  
- Deterministic append semantics  
- No mutation of existing Observations  

### 2.3 ReasoningTree
- Unique structural ID  
- Root ObservationStream  
- Deterministically generated branches  
- Selected branch (lexicographically smallest provenance hash)  
- Tree‑level provenance (aggregated from branches)  
- Semantic hash (derived from selected branch trace)  
- Summary metadata  

---

## 3. Deterministic Interpreter

The interpreter provides:

- `infer()` — single deterministic inference step  
- `chain()` — multi‑step deterministic chain  
- `reason_tree()` — multi‑branch deterministic reasoning tree  

All interpreter behavior is deterministic with respect to:

- input content  
- root context  
- branch index  
- branch depth  

---

## 4. Subsystem 6 — ReasoningTree Semantics

Subsystem 6 defines the deterministic structure and semantics of ReasoningTrees.

### 6.1 Deterministic Branch Generation
- Branch content is deterministically derived from root context + branch index  
- Branch provenance is deterministic  
- Branch confidence is deterministic  
- Branch ordering is deterministic  

### 6.2 Chain Semantics
- Chain depth determines number of inference steps  
- Chain provenance is aggregated deterministically  
- Chain confidence is multiplicative  

### 6.3 Tree‑Level Provenance
- Tree provenance hash is aggregated from final branch hashes  
- Tree provenance confidence is product of branch confidences  
- Summary metadata reflects deterministic structure  

### 6.4 Pruning
- Pruning removes branches below a rank threshold  
- If the previously selected branch is pruned, the top‑ranked branch becomes selected  
- Tree‑level provenance is recomputed after pruning  

### 6.5 Structural Identity
- Tree ID is deterministic and structural  
- Structural identity is preserved across identical inputs  

---

## 6.7 Semantic‑Provenance Lattice  
*(Fully sealed through 6.7.6)*

### **6.7.0 — Semantic Divergence → Provenance Divergence**  
Different meanings produce different provenance hashes.

### **6.7.1 — Semantic Path → Semantic Hash**  
The semantic hash is the SHA‑256 of the selected branch trace contents.

### **6.7.2 — Semantic Stability → Hash Stability**  
Identical semantic paths across trees produce identical semantic hashes.

### **6.7.3 — Semantic Equivalence → Semantic‑Surface Equivalence**  
If two trees share the same semantic hash, then:
- selected branch is identical  
- selected branch trace contents are identical  
- selection justification is identical  

### **6.7.4 — Semantic Equivalence → Confidence Monotonicity**  
For semantically equivalent trees:
- a tree with *more* branches must not have *higher* tree‑level confidence  

### **6.7.5 — Semantic Equivalence → Selected‑Branch Provenance Equivalence**  
For semantically equivalent trees:
- the final provenance hash of the selected branch is identical  

### **6.7.6 — Semantic Equivalence → Semantic Identity Equivalence**  
The semantic hash itself serves as the canonical semantic identity.  
Semantically equivalent trees therefore share the same semantic identity.

---

## Status
Subsystem 6.7 is fully sealed.  
All invariants are satisfied by the current implementation.  
Next subsystem: **6.8 — TBD (Semantic Compression / Provenance Anchoring)**.

Patrick — this is the moment where Subsystem 6.8 becomes part of the *canonical* TESLA Protocol.  
You’ve built something stable, deterministic, and elegant — and now we’re going to capture it cleanly in the documentation so future‑you (and future agents) can stand on solid ground.

Below is a **drop‑in, fully‑formed update** for both **TESLA_PROTOCOL.md** and **README.md**, written in the same authoritative, structural voice as the rest of your protocol docs.  
No fluff. No drift. Just clean, canonical state.

---

# 📘 **TESLA_PROTOCOL.md — Subsystem 6.8 Update (Drop‑In)**

Insert this as the complete definition of **Subsystem 6.8**:

---

## **6.8 — Semantic Compression Layer**

Subsystem 6.8 introduces a deterministic semantic‑compression surface for ReasoningTrees.  
This layer produces a canonical semantic fingerprint that is invariant under:

- branch count  
- pruning  
- interpreter counters  
- structural differences  
- non‑semantic variation  

All invariants in 6.8 operate exclusively on the **selected branch trace**, ensuring that semantic identity is derived from meaning, not structure.

---

### **6.8.0 — Semantic Summary Stability**

Every ReasoningTree must expose a `semantic_summary` field inside its `summary` dictionary.

This field must be present for all trees and must be stable across semantically equivalent trees.

---

### **6.8.1 — Normalized Semantic Tokens**

`semantic_summary` must include a normalized token list derived from the selected branch trace.

Normalization rules:

- lowercase  
- alphanumeric only  
- extracted deterministically from concatenated observation contents  

Structure:

```json
"semantic_summary": {
  "hash": "<semantic_hash>",
  "tokens": ["token1", "token2", ...]
}
```

---

### **6.8.2 — Token Frequencies**

`semantic_summary` must include a deterministic histogram of normalized tokens.

Structure:

```json
"semantic_summary": {
  "hash": "<semantic_hash>",
  "tokens": [...],
  "token_frequencies": {
    "token": count,
    ...
  }
}
```

Frequencies must match the exact counts of normalized tokens.

---

### **6.8.3 — Stable Semantic Fingerprint**

`semantic_summary` must include a canonical semantic fingerprint.

Definition:

- expand each token according to its frequency  
- sort lexicographically  
- join with `-`  

Structure:

```json
"semantic_summary": {
  "hash": "<semantic_hash>",
  "tokens": [...],
  "token_frequencies": {...},
  "fingerprint": "anchor-branch-branch-derived-..."
}
```

This fingerprint is a deterministic semantic signature.

---

### **6.8.4 — Semantic Summary Stability Across Equivalent Trees**

For any two ReasoningTrees with identical `tree_provenance_hash` values:

- the entire `semantic_summary` dictionary must be identical  
- including `hash`, `tokens`, `token_frequencies`, and `fingerprint`  

This invariant seals Subsystem 6.8 as a stable semantic‑identity layer.

---

## **6.9 — Provenance‑Weighted Semantic Compression**

Subsystem 6.9 extends the semantic‑compression layer (6.8) by incorporating *provenance confidence* into the semantic identity surface. This produces a second, epistemic fingerprint and hash that reflect not only *what* the tree means, but *how strongly* that meaning is supported by its provenance.

All invariants in 6.9 operate exclusively on the **selected branch trace**, ensuring that provenance‑weighted semantics remain stable under structural variation, branch count, and pruning.

---

### **6.9.0 — Provenance‑Weighted Token Scores**

`semantic_summary` must include a dictionary mapping each normalized token to a provenance‑weighted score.

Definition:

- For each observation in the selected branch trace:
  - normalize its tokens using the same rules as 6.8.1  
  - each token inherits the observation’s provenance confidence  
  - token score = sum of confidences across all occurrences

Structure:

```json
"provenance_weighted_tokens": {
  "token": float_score,
  ...
}
```

Scores must be positive floats.

---

### **6.9.1 — Provenance‑Weighted Fingerprint**

`semantic_summary` must include a provenance‑weighted fingerprint.

Definition:

- sort tokens by:
  1. descending provenance‑weighted score  
  2. ascending lexicographic order  
- join tokens with `-`

Structure:

```json
"provenance_fingerprint": "tokenA-tokenB-tokenC-..."
```

This fingerprint is a deterministic epistemic signature.

---

### **6.9.2 — Provenance‑Weighted Semantic Hash**

`semantic_summary` must include a provenance‑weighted semantic hash.

Definition:

- construct sorted `"token:score"` pairs  
- join with `"|"`  
- compute SHA‑256 of the resulting string  

Structure:

```json
"provenance_weighted_hash": "<sha256_hex>"
```

This hash is the epistemic counterpart to the semantic hash defined in 6.8.3.

---

### **6.9.3 — Provenance‑Semantic Stability Across Equivalent Trees**

For any two ReasoningTrees with identical `tree_provenance_hash` values (semantic equivalence):

- their `provenance_weighted_hash` values must also be identical  
- their `provenance_fingerprint` values must also be identical  
- their `provenance_weighted_tokens` dictionaries must match exactly  

This invariant ensures that provenance‑weighted semantics are a *pure function of meaning*, independent of:

- branch count  
- pruning  
- structural variation  
- interpreter counters  

Subsystem 6.9 is sealed when all four invariants hold.
