

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class ScoreRecord:
    """
    Minimal, structured scoring output for one generated attack case.

    v0 behavior: produces placeholder scores (all zeros) so the pipeline is end-to-end runnable.
    Later: replace `score_case()` with real policy/guardrail/persistence logic and/or model outputs.
    """
    attack_id: str
    seed: int
    turn_count: int
    policy_violation: int  # 0/1
    guardrail_bypass: int  # 0/1
    severity: int          # 0-3 (placeholder)
    persistence: int       # 0/1 (placeholder)
    notes: str = ""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, obj: Any, pretty: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        if pretty:
            json.dump(obj, f, indent=2, sort_keys=True)
        else:
            json.dump(obj, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")


def score_case(case: Dict[str, Any]) -> ScoreRecord:
    """
    Score a single attack case.

    IMPORTANT: This is intentionally a placeholder implementation.
    It verifies schema assumptions and emits a stable, structured score record.

    Inputs expected from generator:
      - attack_id (str)
      - seed (int)
      - turns (list)
    """
    attack_id = str(case.get("attack_id", ""))
    seed = int(case.get("seed", 0))
    turns = case.get("turns", [])
    turn_count = int(len(turns)) if isinstance(turns, list) else 0

    # Placeholder scoring (v0)
    return ScoreRecord(
        attack_id=attack_id,
        seed=seed,
        turn_count=turn_count,
        policy_violation=0,
        guardrail_bypass=0,
        severity=0,
        persistence=0,
        notes="placeholder_v0",
    )


def evaluate(attacks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Evaluate a list of attack cases and return a list of score dicts.
    """
    scores: List[Dict[str, Any]] = []
    for case in attacks:
        rec = score_case(case)
        scores.append(asdict(rec))
    return scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate generated attack cases (v0 placeholder scorer).")
    parser.add_argument(
        "--in",
        dest="in_path",
        default="reports/raw_attacks.json",
        help="Path to input attack cases JSON (array). Default: reports/raw_attacks.json",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default="reports/scores.json",
        help="Path to output scores JSON (array). Default: reports/scores.json",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    args = parser.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    data = load_json(in_path)

    # Accept either a single case object or an array of cases
    if isinstance(data, dict):
        attacks = [data]
    elif isinstance(data, list):
        attacks = data
    else:
        raise SystemExit("Input JSON must be an object or an array of objects.")

    scores = evaluate(attacks)
    dump_json(out_path, scores, pretty=args.pretty)

    print(f"Wrote {len(scores)} score records -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())