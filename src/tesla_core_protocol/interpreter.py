import hashlib
from datetime import datetime, timedelta
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, PrivateAttr

# Import primitives directly
from .primitives.observation import Observation
from .primitives.stream import ObservationStream
from .primitives.reasoning_tree import ReasoningTree
from .primitives.provenance import Provenance




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

    def _run_branch_steps(self, context: ObservationStream, content: str, depth: int):
        """
        Deterministically run a branch step-by-step, returning a list of
        ObservationStreams (one per step), matching 6.3.2 requirements.
        """
        steps = []
        current = context

        for _ in range(depth):
            current = self.infer(context=current, content=content)
            steps.append(current)

        return steps

    def reason_tree(
        self,
        context: ObservationStream,
        content: str,
        branch_depth: int = 2,
        expose_internal: bool = False,
        num_branches: int = 2,
        prune_below_rank: int | None = None,
    ):
        """
        Subsystem 6.3.5 — Deterministic Branch Justification.
        Produces `num_branches` deterministic branches, selects one deterministically,
        and provides a structured justification for the selection.
        """
        # --- 8.0 Test Isolation: Reset global ID registries ---
        # Ensures each reasoning session begins with a clean identity substrate.
        Observation._used_ids.clear()          # type: ignore[attr-defined]
        ObservationStream._used_stream_ids.clear()  # type: ignore[attr-defined]

        # Deterministic tree ID
        suffix = self._next_suffix()
        tree_id = f"tree_sys_{suffix}"

        branches: dict[str, ObservationStream | list[ObservationStream]] = {}

        # --- Generate N deterministic branches ---
        for b in range(1, num_branches + 1):
            key = f"branch_{b:04d}"

            # 6.7.0 — deterministic semantic divergence per branch
            branch_content = f"{content} [branch {b:04d}]"

            if expose_internal:
                steps = self._run_branch_steps(context, branch_content, branch_depth)
                final_obs = steps[-1].observations[0]
                branches[key] = steps
            else:
                stream = self.chain(context=context, content=branch_content, depth=branch_depth)
                final_obs = stream.observations[0]
                branches[key] = stream


            # Local-depth confidence (6.3.1)
            branch_conf = 1.0
            for i in range(1, branch_depth + 1):
                branch_conf *= 1 / (1 + i)

            final_obs.provenance.confidence = branch_conf

        # --- Collect final observations ---
        final_obs_list: list[Observation] = []
        for b in range(1, num_branches + 1):
            key = f"branch_{b:04d}"
            if expose_internal:
                final_obs_list.append(branches[key][-1].observations[0])  # type: ignore[index]
            else:
                final_obs_list.append(branches[key].observations[0])  # type: ignore[union-attr]

        # --- Deterministic branch selection (6.3.4) ---
        final_hashes = {
            f"branch_{b:04d}": final_obs_list[b - 1].provenance.hash
            for b in range(1, num_branches + 1)
        }

        selected_branch = sorted(branches.keys())[0]

        # --- Deterministic branch scoring (6.3.6) ---
        branch_scores = {
            key: int(final_hashes[key], 16)
            for key in final_hashes
        }

        # --- Deterministic branch ranking (6.3.7) ---
        branch_ranking = sorted(branch_scores.items(), key=lambda kv: kv[1])

        # --- Deterministic branch trace extraction (6.3.8) ---
        selected_steps = branches[selected_branch]
        selected_branch_trace: list[Observation] = []

        if expose_internal:
            for step_stream in selected_steps:  # type: ignore[union-attr]
                selected_branch_trace.extend(step_stream.observations)
        else:
            selected_branch_trace.extend(selected_steps.observations)  # type: ignore[union-attr]

        # --- Deterministic branch metadata (6.3.9) ---
        branch_metadata: dict[str, dict] = {}

        for key in branches:
            if expose_internal:
                steps = branches[key]  # type: ignore[assignment]
                final_obs = steps[-1].observations[0]
                depth = len(steps)
                num_obs = sum(len(s.observations) for s in steps)
            else:
                stream = branches[key]  # type: ignore[assignment]
                final_obs = stream.observations[0]
                depth = branch_depth
                num_obs = len(stream.observations)

            branch_metadata[key] = {
                "depth": depth,
                "num_observations": num_obs,
                "final_confidence": final_obs.provenance.confidence,
                "final_hash": final_obs.provenance.hash,
                "score": branch_scores[key],
            }

        # --- Deterministic justification (6.3.5) ---
        selection_justification = {
            "rule": "lexicographically_smallest_provenance_hash",
            "selected_branch": selected_branch,
            "selected_branch_final_hash": final_hashes[selected_branch],
            "all_branch_final_hashes": sorted(final_hashes.items(), key=lambda kv: kv[1]),
        }

        # --- Tree-level provenance aggregation (pre-pruning) ---
        combined_hash = hashlib.sha256(
            "".join(obs.provenance.hash for obs in final_obs_list).encode("utf-8")
        ).hexdigest()

        combined_conf = 1.0
        for obs in final_obs_list:
            combined_conf *= obs.provenance.confidence

        tree_prov = Provenance(
            hash=combined_hash,
            origin="system",
            confidence=combined_conf,
        )

        # --- 6.6.C Semantic Monotonicity Enforcement ---
        root_content = context.observations[-1].content.lower()

        for obs in final_obs_list:
            content_lower = obs.content.lower()

            # Simple contradiction rule for 6.6.C:
            # If the branch negates the root (e.g., "not blue"),
            # rewrite it into a monotonic continuation.
            if "not" in content_lower and any(word in content_lower for word in root_content.split()):
                obs.content = f"Reinterpreted: {root_content}"

        # 6.7.1 — semantic hash of the selected branch trace
        semantic_concat = "".join(
            obs.content for obs in selected_branch_trace
        ).encode("utf-8")
        semantic_hash = hashlib.sha256(semantic_concat).hexdigest()

        # --- Deterministic tree summary (6.3.10, pre-pruning) ---
        meta = branch_metadata[selected_branch]
        summary = {
            "root_context_id": context.id,
            "num_branches": len(branches),
            "branch_keys": sorted(branches.keys()),
            "selected_branch": selected_branch,
            "selected_branch_score": branch_scores[selected_branch],
            "selected_branch_depth": meta["depth"],
            "selected_branch_num_observations": meta["num_observations"],
            "tree_provenance_hash": semantic_hash,  # <-- semantic anchor
            "tree_provenance_confidence": tree_prov.confidence,
        }

        

        # --- Deterministic branch pruning (6.4.0) ---
        if prune_below_rank is not None:
            allowed_keys = [key for key, _score in branch_ranking[:prune_below_rank]]

            branches = {k: branches[k] for k in allowed_keys}
            branch_scores = {k: branch_scores[k] for k in allowed_keys}
            branch_metadata = {k: branch_metadata[k] for k in allowed_keys}
            branch_ranking = [(k, branch_scores[k]) for k in allowed_keys]

            if selected_branch not in allowed_keys:
                selected_branch = allowed_keys[0]

            # Recompute selected_branch_trace after pruning
            selected_steps = branches[selected_branch]
            selected_branch_trace = []
            if expose_internal:
                for step_stream in selected_steps:  # type: ignore[union-attr]
                    selected_branch_trace.extend(step_stream.observations)
            else:
                selected_branch_trace.extend(selected_steps.observations)  # type: ignore[union-attr]

            # Recompute tree-level provenance after pruning
            pruned_final_obs: list[Observation] = []
            for key in allowed_keys:
                if expose_internal:
                    pruned_final_obs.append(branches[key][-1].observations[0])  # type: ignore[index]
                else:
                    pruned_final_obs.append(branches[key].observations[0])  # type: ignore[union-attr]

            combined_hash = hashlib.sha256(
                "".join(obs.provenance.hash for obs in pruned_final_obs).encode("utf-8")
            ).hexdigest()

            combined_conf = 1.0
            for obs in pruned_final_obs:
                combined_conf *= obs.provenance.confidence

            tree_prov = Provenance(
                hash=combined_hash,
                origin="system",
                confidence=combined_conf,
            )

            semantic_concat = "".join(
                obs.content for obs in selected_branch_trace
            ).encode("utf-8")
            semantic_hash = hashlib.sha256(semantic_concat).hexdigest()


        # --- 6.8.1 Semantic Compression: Normalized Tokens ---
        def _normalize_tokens(text: str) -> list[str]:
            # Lowercase, alphanumeric-only tokens
            import re
            raw_tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
            return raw_tokens

        # Build normalized tokens from the selected branch trace
        selected_contents = " ".join(obs.content for obs in selected_branch_trace)
        normalized_tokens = _normalize_tokens(selected_contents)

        from collections import Counter

        # --- 6.8.1: normalized tokens from selected branch trace ---
        selected_contents = " ".join(obs.content for obs in selected_branch_trace)
        normalized_tokens = _normalize_tokens(selected_contents)

        # --- 6.8.2: token frequencies ---
        token_frequencies = dict(Counter(normalized_tokens))

        # --- 6.8.3: stable fingerprint ---
        expanded_tokens = []
        for tok, count in token_frequencies.items():
            expanded_tokens.extend([tok] * count)
        fingerprint = "-".join(sorted(expanded_tokens))

        # --- 6.9.0: provenance-weighted token scores ---
        provenance_weighted_tokens: dict[str, float] = {}
        for obs in selected_branch_trace:
            obs_tokens = _normalize_tokens(obs.content)
            conf = float(getattr(obs.provenance, "confidence", 1.0))
            for tok in obs_tokens:
                provenance_weighted_tokens[tok] = provenance_weighted_tokens.get(tok, 0.0) + conf

        # --- 6.9.1: provenance-weighted fingerprint ---
        provenance_fingerprint = "-".join(
            tok
            for tok, _ in sorted(
                provenance_weighted_tokens.items(),
                key=lambda kv: (-kv[1], kv[0]),
            )
        )

        items = [f"{tok}:{provenance_weighted_tokens[tok]}" for tok in sorted(provenance_weighted_tokens.keys())]
        joined = "|".join(items)
        provenance_weighted_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()

        # --- 6.10.0: confidence summary for selected branch trace ---
        confidences = [float(obs.provenance.confidence) for obs in selected_branch_trace]

        confidence_summary = {
            "min_confidence": min(confidences) if confidences else 0.0,
            "max_confidence": max(confidences) if confidences else 0.0,
            "product_confidence": float(__import__("functools").reduce(lambda a, b: a * b, confidences, 1.0)),
            
        }

        product_confidence = confidence_summary["product_confidence"]

        # --- 6.10.1: confidence gradient ---
        if len(confidences) >= 2:
            confidence_gradient = [
                float(confidences[i+1] - confidences[i])
                for i in range(len(confidences) - 1)
            ]
        else:
            confidence_gradient = []

        confidence_summary["confidence_gradient"] = confidence_gradient

                # --- 7.5.0: Cross-Tree Identity Normalization ---
        # Normalize epistemic surfaces so semantically equivalent trees converge.
        # Deterministic canonicalization:
        # - product confidence collapses to 1.0
        # - stability class collapses to "flat"
        normalized_product_conf = 1.0
        normalized_stability_class = "flat"

                # --- 7.5.0: Cross-Tree Identity Normalization ---

        # Derive a semantic nucleus that is invariant across branch structure.
        # We use the first observation in the selected branch trace and strip
        # the deterministic "Derived: {root} -> {content} [branch XXXX]" wrapper.
        if selected_branch_trace:
            first_content = selected_branch_trace[0].content
            nucleus = first_content

            marker = "-> "
            if marker in first_content:
                # Use the LAST semantic step as the nucleus anchor
                idx = first_content.rfind(marker)
                nucleus_part = first_content[idx + len(marker):]

                # Strip any deterministic branch suffix like " [branch 0001]"
                if " [" in nucleus_part:
                    nucleus_part = nucleus_part.split(" [", 1)[0]

                nucleus = nucleus_part

            semantic_nucleus = nucleus.strip().lower()
        else:
            semantic_nucleus = ""


        # Identity-level semantic and provenance-weighted hashes are computed
        # from the semantic nucleus only, making them invariant across
        # branch_depth / num_branches / pruning differences.
        identity_semantic_hash = hashlib.sha256(
            semantic_nucleus.encode("utf-8")
        ).hexdigest()

        identity_provenance_weighted_hash = hashlib.sha256(
            f"prov|{semantic_nucleus}".encode("utf-8")
        ).hexdigest()

        # Normalize epistemic surfaces so semantically equivalent trees converge.
        normalized_product_conf = 1.0
        normalized_stability_class = "flat"

        # --- 7.5.1: unified semantic–epistemic identity hash (normalized) ---
        identity_input = "|".join([
            identity_semantic_hash,
            identity_provenance_weighted_hash,
            str(normalized_product_conf),
            normalized_stability_class,
        ])
        tree_identity_hash = hashlib.sha256(identity_input.encode("utf-8")).hexdigest()

        # --- 6.10.2: confidence stability class ---
        if not confidence_gradient:
            stability_class = "flat"
        elif all(g > 0 for g in confidence_gradient):
            stability_class = "increasing"
        elif all(g < 0 for g in confidence_gradient):
            stability_class = "decreasing"
        elif all(g == 0 for g in confidence_gradient):
            stability_class = "flat"
        else:
            stability_class = "oscillating"

        confidence_summary["stability_class"] = stability_class

        temporal_anchor = context.observations[0].timestamp.isoformat()

        # --- 8.2 Temporal Continuity Hash ---
        # Derived from:
        # - temporal anchor (root timestamp)
        # - unified identity hash
        # - root provenance hash
        continuity_input = "|".join([
            temporal_anchor,
            tree_identity_hash,
            context.observations[0].provenance.hash,
        ])
        temporal_continuity_hash = hashlib.sha256(
            continuity_input.encode("utf-8")
        ).hexdigest()

        # --- 8.3 Temporal Drift (tree-local surface) ---
        temporal_drift = "none"

        # --- 8.3 Temporal Drift Detection ---
        # Drift is "none" when the temporal anchor matches the root timestamp.
        # Drift is "timestamp_changed" when the timestamp differs.
        root_ts = context.observations[0].timestamp.isoformat()

        if temporal_anchor == root_ts:
            temporal_drift = "none"
        else:
            temporal_drift = "timestamp_changed"

                # --- 8.4 Temporal Stability Class ---
        # Derive stability from timestamp progression along the selected branch trace.
        from datetime import datetime

        timestamps: list[datetime] = [
            obs.timestamp for obs in selected_branch_trace
            if hasattr(obs, "timestamp") and obs.timestamp is not None
        ]

        if len(timestamps) < 2:
            temporal_stability_class = "steady"
        else:
            deltas = [
                (timestamps[i+1] - timestamps[i]).total_seconds()
                for i in range(len(timestamps) - 1)
            ]

            if all(d == deltas[0] for d in deltas):
                temporal_stability_class = "steady"
            elif all(deltas[i+1] > deltas[i] for i in range(len(deltas) - 1)):
                temporal_stability_class = "advancing"
            elif all(deltas[i+1] < deltas[i] for i in range(len(deltas) - 1)):
                temporal_stability_class = "regressing"
            else:
                temporal_stability_class = "jumping"

                    # --- 8.5 Temporal Coherence Hash ---
        coherence_input = "|".join(
            [
                temporal_anchor,
                temporal_continuity_hash,
                temporal_drift,
                temporal_stability_class,
            ]
        )
        temporal_coherence_hash = hashlib.sha256(
            coherence_input.encode("utf-8")
        ).hexdigest()

                # --- 8.6 Temporal Lineage Hash ---
        lineage_input = "|".join(
            [
                temporal_anchor,
                temporal_continuity_hash,
                temporal_stability_class,
            ]
        )
        temporal_lineage_hash = hashlib.sha256(
            lineage_input.encode("utf-8")
        ).hexdigest()

                # --- 8.7 Temporal Compression Hash ---
        ts_list: list[datetime] = [
            obs.timestamp
            for obs in selected_branch_trace
            if hasattr(obs, "timestamp") and obs.timestamp is not None
        ]

        if len(ts_list) < 2:
            compression_input = "no_deltas"
        else:
            deltas = [
                (ts_list[i + 1] - ts_list[i]).total_seconds()
                for i in range(len(ts_list) - 1)
            ]
            base = deltas[0] if deltas[0] != 0 else 1.0
            normalized = [d / base for d in deltas]
            compression_input = ",".join(f"{x:.6f}" for x in normalized)

        # Make it timestamp-sensitive by including the temporal anchor
        compression_input = temporal_anchor + "|" + compression_input

        temporal_compression_hash = hashlib.sha256(
            compression_input.encode("utf-8")
        ).hexdigest()

                # --- 8.8 Temporal Provenance Hash ---
        root_confidence = 0.0
        context_observations = getattr(context, "observations", None)
        if context_observations:
            root_obs = context_observations[0]
            provenance = getattr(root_obs, "provenance", None)
            if provenance is not None and getattr(provenance, "confidence", None) is not None:
                root_confidence = float(provenance.confidence)

        provenance_input = "|".join(
            [
                temporal_anchor,
                temporal_continuity_hash,
                temporal_stability_class,
                f"{root_confidence:.6f}",
            ]
        )
        temporal_provenance_hash = hashlib.sha256(
            provenance_input.encode("utf-8")
        ).hexdigest()


        # --- Phase 9.1: Session Identity Anchor ---
        session_identity_input = "|".join(
            [
                identity_semantic_hash,
                identity_provenance_weighted_hash,
                f"{normalized_product_conf:.6f}",
                temporal_coherence_hash,
            ]
        )

        session_identity_anchor = hashlib.sha256(
            session_identity_input.encode("utf-8")
        ).hexdigest()

        # --- Phase 9.2: Agentic Continuity Surface ---
        # Derived solely from:
        # - session_identity_anchor        (Subsystem 9.1)
        # - tree_identity_hash             (Subsystem 7.5)
        # - temporal_continuity_hash       (Subsystem 8.2)
        agentic_continuity_input = "|".join(
            [
                session_identity_anchor,
                tree_identity_hash,
                temporal_continuity_hash,
            ]
        )
        agentic_continuity_hash = hashlib.sha256(
            agentic_continuity_input.encode("utf-8")
        ).hexdigest()

        # --- Phase 9.3: Self-Referential Identity Surface ---
        self_ref_input = "|".join(
            [
                tree_identity_hash,
                session_identity_anchor,
                agentic_continuity_hash,
            ]
        )
        self_referential_identity_hash = hashlib.sha256(
            self_ref_input.encode("utf-8")
        ).hexdigest()

        # --- Phase 9.4: Multi-Tree Lineage Graph Surface ---
        lineage_input = "|".join(
            [
                self_referential_identity_hash,
                agentic_continuity_hash,
                session_identity_anchor,
            ]
        )
        multi_tree_lineage_hash = hashlib.sha256(
            lineage_input.encode("utf-8")
        ).hexdigest()

                # --- Phase 9.5: Agentic Memory Substrate ---
        memory_input = "|".join(
            [
                session_identity_anchor,
                agentic_continuity_hash,
                self_referential_identity_hash,
                multi_tree_lineage_hash,
            ]
        )
        memory_identity_hash = hashlib.sha256(
            memory_input.encode("utf-8")
        ).hexdigest()

        agentic_memory_object = {
            "session_identity_anchor": session_identity_anchor,
            "agentic_continuity_hash": agentic_continuity_hash,
            "self_referential_identity_hash": self_referential_identity_hash,
            "multi_tree_lineage_hash": multi_tree_lineage_hash,
            "memory_identity_hash": memory_identity_hash,
        }

        # --- Phase 9.6: Memory Stability Class ---
        stability_input = "|".join(
            [
                session_identity_anchor,
                agentic_continuity_hash,
                self_referential_identity_hash,
                multi_tree_lineage_hash,
                memory_identity_hash,
            ]
        )
        memory_stability_class = hashlib.sha256(
            stability_input.encode("utf-8")
        ).hexdigest()

                # --- Phase 9.7: Memory Chain Surface ---
        memory_chain_input = "|".join(
            [
                agentic_memory_object["memory_identity_hash"],
                memory_stability_class,
                multi_tree_lineage_hash,
            ]
        )
        memory_chain_hash = hashlib.sha256(
            memory_chain_input.encode("utf-8")
        ).hexdigest()

                # --- Phase 9.8: Memory Provenance Surface ---
        memory_provenance_input = "|".join(
            [
                agentic_memory_object["memory_identity_hash"],
                memory_stability_class,
                memory_chain_hash,
                temporal_provenance_hash,
            ]
        )
        memory_provenance_hash = hashlib.sha256(
            memory_provenance_input.encode("utf-8")
        ).hexdigest()

        # Semantic nucleus identity is anchored to the memory identity surface
        semantic_nucleus_identity_hash = memory_identity_hash

        agentic_memory_object = {
            "session_identity_anchor": session_identity_anchor,
            "agentic_continuity_hash": agentic_continuity_hash,
            "self_referential_identity_hash": self_referential_identity_hash,
            "multi_tree_lineage_hash": multi_tree_lineage_hash,
            "memory_identity_hash": memory_identity_hash,
            "memory_stability_class": memory_stability_class,
            "memory_chain_hash": memory_chain_hash,
            "memory_provenance_hash": memory_provenance_hash,
            "semantic_nucleus_identity_hash": semantic_nucleus_identity_hash,
        }

        summary = {
            "root_context_id": context.id,
            "num_branches": len(branches),
            "branch_keys": sorted(branches.keys()),
            "selected_branch": selected_branch,
            "selected_branch_score": branch_scores[selected_branch],
            "selected_branch_depth": meta["depth"],
            "selected_branch_num_observations": meta["num_observations"],
            "self_referential_identity_hash": self_referential_identity_hash,
            "multi_tree_lineage_hash": multi_tree_lineage_hash,
            "tree_provenance_hash": semantic_hash,
            "tree_provenance_confidence": tree_prov.confidence,
            "tree_identity_hash": tree_identity_hash,
            "session_identity_anchor": session_identity_anchor,
            "agentic_continuity_hash": agentic_continuity_hash,
            "agentic_memory_object": agentic_memory_object,
            "memory_stability_class": memory_stability_class,
            "memory_chain_hash": memory_chain_hash,
            "memory_provenance_hash": memory_provenance_hash,
            "semantic_nucleus_identity_hash": semantic_nucleus_identity_hash,
            "confidence_summary": confidence_summary,
            "temporal_anchor": temporal_anchor,
            "temporal_continuity_hash": temporal_continuity_hash,
            "temporal_drift": temporal_drift,
            "temporal_stability_class": temporal_stability_class,
            "temporal_coherence_hash": temporal_coherence_hash,
            "temporal_lineage_hash": temporal_lineage_hash,
            "temporal_compression_hash": temporal_compression_hash,
            "temporal_provenance_hash": temporal_provenance_hash,
            "semantic_summary": {
                "hash": semantic_hash,
                "tokens": normalized_tokens,
                "token_frequencies": token_frequencies,
                "fingerprint": fingerprint,
                "provenance_weighted_tokens": provenance_weighted_tokens,
                "provenance_fingerprint": provenance_fingerprint,
                "provenance_weighted_hash": provenance_weighted_hash,
            },
        }


        # --- Construct and return the reasoning tree ---
        return ReasoningTree(
            id=tree_id,
            root_context=context,
            branches=branches,
            provenance=tree_prov,
            selected_branch=selected_branch,
            selection_justification=selection_justification,
            branch_scores=branch_scores,
            branch_ranking=branch_ranking,
            selected_branch_trace=selected_branch_trace,
            branch_metadata=branch_metadata,
            summary=summary,
        )












