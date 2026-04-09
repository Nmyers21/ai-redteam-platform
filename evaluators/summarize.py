from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCORES_PATH = PROJECT_ROOT / "reports" / "scores.json"
DEFAULT_SUMMARY_JSON_PATH = PROJECT_ROOT / "reports" / "summary.json"
DEFAULT_SUMMARY_MD_PATH = PROJECT_ROOT / "reports" / "summary.md"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def dump_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def as_score_list(payload: Any, *, name: str) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    raise SystemExit(f"{name} must be a JSON array of score objects.")


def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def safe_float(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def rate(records: List[Dict[str, Any]], key: str) -> Optional[float]:
    present = [record.get(key) for record in records if record.get(key) is not None]
    if not present:
        return None
    positives = sum(1 for value in present if int(value) == 1)
    return positives / len(present)


def format_pct(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def format_num(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def summarize_scores(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_cases = len(scores)

    mode_counts = Counter(str(record.get("scoring_mode", "unknown")) for record in scores)
    severity_counts = Counter(int(record.get("severity", 0)) for record in scores)
    attack_surface_counts = Counter(int(record.get("attack_surface_score", 0)) for record in scores)

    attack_surface_values = [
        value for value in (safe_float(record.get("attack_surface_score")) for record in scores)
        if value is not None
    ]
    severity_values = [
        value for value in (safe_float(record.get("severity")) for record in scores)
        if value is not None
    ]
    turn_counts = [
        value for value in (safe_float(record.get("turn_count")) for record in scores)
        if value is not None
    ]

    evidence_counter: Counter[str] = Counter()
    for record in scores:
        evidence = record.get("evidence", [])
        if isinstance(evidence, list):
            for item in evidence:
                if isinstance(item, str) and item:
                    evidence_counter[item] += 1

    summary: Dict[str, Any] = {
        "generated_utc": utc_now_iso(),
        "total_cases": total_cases,
        "mode_counts": dict(mode_counts),
        "avg_attack_surface_score": mean(attack_surface_values),
        "avg_severity": mean(severity_values),
        "avg_turn_count": mean(turn_counts),
        "policy_violation_rate": rate(scores, "policy_violation"),
        "guardrail_bypass_rate": rate(scores, "guardrail_bypass"),
        "persistence_rate": rate(scores, "persistence"),
        "severity_distribution": {str(key): severity_counts[key] for key in sorted(severity_counts)},
        "attack_surface_distribution": {str(key): attack_surface_counts[key] for key in sorted(attack_surface_counts)},
        "top_evidence": [
            {"signal": signal, "count": count}
            for signal, count in evidence_counter.most_common(10)
        ],
    }
    return summary


def compare_summaries(baseline: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    delta: Dict[str, Any] = {}

    numeric_metrics = (
        "avg_attack_surface_score",
        "avg_severity",
        "avg_turn_count",
        "policy_violation_rate",
        "guardrail_bypass_rate",
        "persistence_rate",
    )

    for metric in numeric_metrics:
        base_value = safe_float(baseline.get(metric))
        candidate_value = safe_float(candidate.get(metric))
        if base_value is None or candidate_value is None:
            delta[metric] = None
        else:
            delta[metric] = candidate_value - base_value

    return delta


def build_markdown_report(
    candidate: Dict[str, Any],
    *,
    baseline: Optional[Dict[str, Any]] = None,
    delta: Optional[Dict[str, Any]] = None,
) -> str:
    lines: List[str] = []
    lines.append("# Evaluation Summary")
    lines.append("")
    lines.append(f"- generated_utc: {candidate.get('generated_utc')}")
    lines.append(f"- total_cases: {candidate.get('total_cases')}")
    lines.append(f"- scoring_modes: {candidate.get('mode_counts')}")
    lines.append("")
    lines.append("## Core Metrics")
    lines.append("")
    lines.append(f"- avg_attack_surface_score: {format_num(safe_float(candidate.get('avg_attack_surface_score')))}")
    lines.append(f"- avg_severity: {format_num(safe_float(candidate.get('avg_severity')))}")
    lines.append(f"- avg_turn_count: {format_num(safe_float(candidate.get('avg_turn_count')))}")
    lines.append(f"- policy_violation_rate: {format_pct(safe_float(candidate.get('policy_violation_rate')))}")
    lines.append(f"- guardrail_bypass_rate: {format_pct(safe_float(candidate.get('guardrail_bypass_rate')))}")
    lines.append(f"- persistence_rate: {format_pct(safe_float(candidate.get('persistence_rate')))}")
    lines.append("")

    lines.append("## Distributions")
    lines.append("")
    lines.append(f"- severity_distribution: {candidate.get('severity_distribution')}")
    lines.append(f"- attack_surface_distribution: {candidate.get('attack_surface_distribution')}")
    lines.append("")

    lines.append("## Top Evidence Signals")
    lines.append("")
    top_evidence = candidate.get("top_evidence", [])
    if isinstance(top_evidence, list) and top_evidence:
        for item in top_evidence:
            if isinstance(item, dict):
                lines.append(f"- {item.get('signal')}: {item.get('count')}")
    else:
        lines.append("- n/a")
    lines.append("")

    if baseline is not None and delta is not None:
        lines.append("## Baseline Comparison")
        lines.append("")
        lines.append(f"- baseline_total_cases: {baseline.get('total_cases')}")
        for key, value in delta.items():
            numeric_value = safe_float(value)
            if numeric_value is None:
                lines.append(f"- delta_{key}: n/a")
            elif key.endswith("_rate"):
                lines.append(f"- delta_{key}: {numeric_value * 100:.2f} percentage points")
            else:
                lines.append(f"- delta_{key}: {numeric_value:.3f}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate aggregate metrics from evaluator score records.")
    parser.add_argument(
        "--in",
        dest="in_path",
        default=str(DEFAULT_SCORES_PATH),
        help="Path to score records JSON (array). Default: repo_root/reports/scores.json",
    )
    parser.add_argument(
        "--compare",
        dest="compare_path",
        default="",
        help="Optional baseline score records JSON for before/after delta comparison.",
    )
    parser.add_argument(
        "--out-json",
        dest="out_json_path",
        default=str(DEFAULT_SUMMARY_JSON_PATH),
        help="Path to summary JSON output. Default: repo_root/reports/summary.json",
    )
    parser.add_argument(
        "--out-md",
        dest="out_md_path",
        default=str(DEFAULT_SUMMARY_MD_PATH),
        help="Path to markdown summary output. Default: repo_root/reports/summary.md",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print summary JSON.")
    args = parser.parse_args()

    candidate_scores = as_score_list(load_json(Path(args.in_path)), name="--in")
    candidate_summary = summarize_scores(candidate_scores)

    payload: Dict[str, Any] = {"summary": candidate_summary}
    baseline_summary: Optional[Dict[str, Any]] = None
    delta: Optional[Dict[str, Any]] = None

    if args.compare_path:
        baseline_scores = as_score_list(load_json(Path(args.compare_path)), name="--compare")
        baseline_summary = summarize_scores(baseline_scores)
        delta = compare_summaries(baseline_summary, candidate_summary)
        payload["baseline_summary"] = baseline_summary
        payload["delta"] = delta

    dump_json(Path(args.out_json_path), payload, pretty=args.pretty)
    markdown = build_markdown_report(candidate_summary, baseline=baseline_summary, delta=delta)
    dump_text(Path(args.out_md_path), markdown)

    print(f"Wrote summary JSON -> {args.out_json_path}")
    print(f"Wrote summary Markdown -> {args.out_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
