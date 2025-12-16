from __future__ import annotations

# --- Imports standard libraries only ---
import argparse
import hashlib
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# --- Constants ---
SCHEMA_VERSION = "v0" 
GENERATOR_VERSION = "0.1.0"

ADVERSARIES = [
    "Casual Policy Tester",
    "Persistent Jailbreaker",
    "Indirect Prompt Injector",
    "Semantic Obfuscator",
]

ATTACK_FAMILIES = [
    "prompt Injection",
    "semantic_obfuscation",
    "multi_turn_escalation",
    "formatting_variance",
]

# Content-agnostic mutation catalog
MUTATION_CATALOG = [
    "structural_reframing",
    "instruction_nesting",
    "contextual_role_confusion",
    "paraphrasing",
    "translation_roundtrip",
    "formatting_variance",
    "token_boundary_manipulation",
]



# --- Data Models
@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    mutation_type: str
    params: Dict[str, Any]
    order: int


@dataclass(frozen=True)
class Turn:
    turn_index: int
    role: str
    content: str
    notes: str = ""


@dataclass(frozen=True)
class AttackCase:
    attack_id: str
    schema_version: str
    seed: int
    created_utc: str

    adversary: str
    attack_family: str

    base_prompt_id: str
    mutations: List[Mutation]
    turns: List[Turn]

    expected_failure_modes: List[str]
    metadata: Dict[str, Any]

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stable_hash_id(seed: int, adversary: str, attack_family: str, base_prompt_id: str, mutation_types: List[str]) -> str:
    """
    Creates a stable ID from deterministic inputs.
    """
    material = {
        "seed": seed,
        "adversary": adversary,
        "attack_family": attack_family,
        "base_prompt_id": base_prompt_id,
        "mutation_types": mutation_types,
        "schema_version": SCHEMA_VERSION,
    }
    blob = json.dumps(material, sort_keys=True, seperators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]

def generate_one(seed: int) -> AttackCase:
    rng = random.Random(seed)

    adversary = rng.choice(ADVERSARIES)
    attack_family = rng.choice(ATTACK_FAMILIES)

    base_prompt_id = "base_prompt_001"

    mutation_catalog = [
        "structural_reframing",
        "instruction_nesting",
        "contextual_role_confusion",
        "paraphrasing",
        "translation_roundtrip",
        "formatting_variance",
        "token_boundary_manipulation",
    ]

    chosen = rng.sample(mutation_catalog, k=2)

    mutations: List[Mutation] = []
    for i, mtype in enumerate(chosen, start=1):
        mutations.append(
            Mutation(
                mutation_id=f"m{i:02d}",
                mutation_type=mtype,
                params={"note": "placeholder"},
                order=i,
            )
        )

    attack_id = stable_hash_id(seed, adversary, attack_family, base_prompt_id, chosen)

    turns = [
        Turn(
            turn_index=0,
            role="user",
            content="BENIGN_BASE_PROMPT_PLACEHOLDER",
            notes="This is a placeholder; later replaced by mutated prompt text.",
        )
    ]

    expected_failure_modes = [
        "policy_violation",
        "instruction_hierarchy_confusion",
        "multi_turn_persistence",
    ]

    metadata = {
        "language": "en",
        "encoding": "plain",
        "mutation_depth": len(mutations),
    }

    return AttackCase(
        attack_id=attack_id,
        schema_version=SCHEMA_VERSION,
        seed=seed,
        created_utc=utc_now_iso(),
        adversary=adversary,
        attack_family=attack_family,
        base_prompt_id=base_prompt_id,
        mutations=mutations,
        turns=turns,
        expected_failure_modes=expected_failure_modes,
        metadata=metadata,
    )

def to_json(case: AttackCase) -> str:
    def convert(obj: Any) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        return obj
    payload = convert(case)
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one deterministic attack case (stub).")
    parser.add_argument("--seed", type=int, default=1337, help="Deterministic seed.")
    args = parser.parse_args()

    case = generate_one(args.seed)
    print(to_json(case))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

