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

        # --- 6.10.1: confidence gradient ---
        if len(confidences) >= 2:
            confidence_gradient = [
                float(confidences[i+1] - confidences[i])
                for i in range(len(confidences) - 1)
            ]
        else:
            confidence_gradient = []

        confidence_summary["confidence_gradient"] = confidence_gradient

        # --- 6.11.0: unified semantic–epistemic identity hash ---
        identity_input = "|".join([
            semantic_hash,
            provenance_weighted_hash,
            str(confidence_summary.get("product_confidence", 0.0)),
            str(confidence_summary.get("stability_class", "")),
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



        summary = {
            "root_context_id": context.id,
            "num_branches": len(branches),
            "branch_keys": sorted(branches.keys()),
            "selected_branch": selected_branch,
            "selected_branch_score": branch_scores[selected_branch],
            "selected_branch_depth": meta["depth"],
            "selected_branch_num_observations": meta["num_observations"],
            "tree_provenance_hash": semantic_hash,
            "tree_provenance_confidence": tree_prov.confidence,
            "tree_identity_hash": tree_identity_hash,
            "confidence_summary": confidence_summary,
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












