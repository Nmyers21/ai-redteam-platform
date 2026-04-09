from __future__ import annotations

# --- Imports standard libraries only ---
import argparse
import hashlib
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --- Constants ---
SCHEMA_VERSION = "v1"
GENERATOR_VERSION = "0.2.0"

ADVERSARIES = [
    "Casual Policy Tester",
    "Persistent Jailbreaker",
    "Indirect Prompt Injector",
    "Semantic Obfuscator",
]

ATTACK_FAMILIES = [
    "prompt_injection",
    "semantic_obfuscation",
    "multi_turn_escalation",
    "formatting_variance",
]

MUTATION_CATALOG = [
    "structural_reframing",
    "instruction_nesting",
    "contextual_role_confusion",
    "paraphrasing",
    "translation_roundtrip",
    "formatting_variance",
    "token_boundary_manipulation",
]

# Valid (attack_family, adversary) combos that have real prompts
VALID_COMBOS: List[Tuple[str, str]] = [
    ("prompt_injection",      "Indirect Prompt Injector"),
    ("prompt_injection",      "Persistent Jailbreaker"),
    ("semantic_obfuscation",  "Semantic Obfuscator"),
    ("semantic_obfuscation",  "Casual Policy Tester"),
    ("multi_turn_escalation", "Persistent Jailbreaker"),
    ("multi_turn_escalation", "Indirect Prompt Injector"),
    ("formatting_variance",   "Semantic Obfuscator"),
    ("formatting_variance",   "Casual Policy Tester"),
]


# --- Data Models ---
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


def stable_hash_id(
    seed: int,
    adversary: str,
    attack_family: str,
    base_prompt_id: str,
    mutation_types: List[str],
    turn_count: int,
) -> str:
    material = {
        "schema_version": SCHEMA_VERSION,
        "seed": seed,
        "adversary": adversary,
        "attack_family": attack_family,
        "base_prompt_id": base_prompt_id,
        "mutation_types": mutation_types,
        "turn_count": turn_count,
    }
    blob = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def build_turns_from_prompt(turn_contents: List[str]) -> List[Turn]:
    return [
        Turn(
            turn_index=i,
            role="user",
            content=content,
            notes="Real attack prompt from library.",
        )
        for i, content in enumerate(turn_contents)
    ]


def generate_one(
    seed: int,
    created_utc: Optional[str] = None,
    attack_family: Optional[str] = None,
    adversary: Optional[str] = None,
) -> AttackCase:
    # Import here so generate.py still works standalone if attack_prompts isn't present
    try:
        from attack_prompts import get_prompts_for
    except ImportError:
        from generators.attack_prompts import get_prompts_for

    rng = random.Random(seed)

    # Pick a valid combo that has real prompts
    if attack_family and adversary:
        combo = (attack_family, adversary)
    elif attack_family:
        candidates = [(f, a) for f, a in VALID_COMBOS if f == attack_family]
        combo = rng.choice(candidates) if candidates else rng.choice(VALID_COMBOS)
    else:
        combo = rng.choice(VALID_COMBOS)

    chosen_family, chosen_adversary = combo
    prompts = get_prompts_for(chosen_family, chosen_adversary)

    if not prompts:
        raise ValueError(f"No prompts for ({chosen_family}, {chosen_adversary})")

    base_prompt_id, turn_contents = rng.choice(prompts)
    turns_list = build_turns_from_prompt(turn_contents)

    chosen_mutations = rng.sample(MUTATION_CATALOG, k=2)
    mutations: List[Mutation] = [
        Mutation(
            mutation_id=f"m{i:02d}",
            mutation_type=mtype,
            params={"strategy_profile": f"{mtype}_baseline"},
            order=i,
        )
        for i, mtype in enumerate(chosen_mutations, start=1)
    ]

    attack_id = stable_hash_id(
        seed,
        chosen_adversary,
        chosen_family,
        base_prompt_id,
        chosen_mutations,
        len(turns_list),
    )

    expected_failure_modes = [
        "policy_violation",
        "instruction_hierarchy_confusion",
        "multi_turn_persistence",
    ]

    metadata = {
        "language": "en",
        "encoding": "plain",
        "mutation_depth": len(mutations),
        "turn_count": len(turns_list),
        "generator_version": GENERATOR_VERSION,
    }

    return AttackCase(
        attack_id=attack_id,
        schema_version=SCHEMA_VERSION,
        seed=seed,
        created_utc=created_utc or utc_now_iso(),
        adversary=chosen_adversary,
        attack_family=chosen_family,
        base_prompt_id=base_prompt_id,
        mutations=mutations,
        turns=turns_list,
        expected_failure_modes=expected_failure_modes,
        metadata=metadata,
    )


def to_json(case: AttackCase, pretty: bool = True) -> str:
    payload = asdict(case)
    if pretty:
        return json.dumps(payload, indent=2, sort_keys=True)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def dump_output(path: Path, output: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output + "\n", encoding="utf-8")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "raw_attacks.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate real LLM attack cases.")
    parser.add_argument("--seed", type=int, default=1337, help="Deterministic seed.")
    parser.add_argument("--count", type=int, default=5, help="Number of cases to generate (>=1).")
    parser.add_argument("--attack-family", type=str, default="", help=f"Filter by family. Choices: {ATTACK_FAMILIES}")
    parser.add_argument("--adversary", type=str, default="", help=f"Filter by adversary. Choices: {ADVERSARIES}")
    parser.add_argument("--created-utc", type=str, default="", help="Fixed UTC timestamp for reproducibility.")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON output.")
    parser.add_argument(
        "--out",
        type=str,
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    args = parser.parse_args()

    if args.count < 1:
        raise SystemExit("--count must be >= 1")

    cases: List[AttackCase] = []
    for i in range(args.count):
        cases.append(
            generate_one(
                seed=args.seed + i,
                created_utc=args.created_utc or None,
                attack_family=args.attack_family or None,
                adversary=args.adversary or None,
            )
        )

    payload = [asdict(c) for c in cases]
    output = json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True)

    out_path = Path(args.out)
    dump_output(out_path, output)
    print(f"Wrote {len(cases)} attack case(s) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())