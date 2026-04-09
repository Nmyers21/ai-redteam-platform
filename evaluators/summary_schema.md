# Evaluator Summary Schema

`evaluators/summarize.py` writes a JSON payload with:

- `summary`: aggregate metrics for the input score file
- optional `baseline_summary`: aggregate metrics for the `--compare` score file
- optional `delta`: candidate minus baseline metric deltas

## `summary` / `baseline_summary` Fields

- `generated_utc`: timestamp string
- `total_cases`: integer
- `mode_counts`: object keyed by scoring mode
- `avg_attack_surface_score`: number or `null`
- `avg_severity`: number or `null`
- `avg_turn_count`: number or `null`
- `policy_violation_rate`: number in `[0,1]` or `null`
- `guardrail_bypass_rate`: number in `[0,1]` or `null`
- `persistence_rate`: number in `[0,1]` or `null`
- `severity_distribution`: object mapping severity values to counts
- `attack_surface_distribution`: object mapping surface scores to counts
- `top_evidence`: array of `{signal, count}` objects

## `delta` Fields

Each delta value is `candidate_metric - baseline_metric` or `null` if unavailable:

- `avg_attack_surface_score`
- `avg_severity`
- `avg_turn_count`
- `policy_violation_rate`
- `guardrail_bypass_rate`
- `persistence_rate`
