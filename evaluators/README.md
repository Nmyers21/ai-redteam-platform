# Evaluators

The evaluator converts generated attack cases into deterministic score records.

## Supported Modes

### Attack-Only

Use this when you only have generated attack cases. The evaluator estimates attack pressure and persistence risk, but observed failure fields remain `null`.

### Response-Aware

Use this when assistant outputs are attached to the case. The evaluator looks for refusal signals, procedural compliance, and multi-turn escalation patterns.

## Accepted Input Shapes

The evaluator accepts either:

- a single case object
- an array of case objects

Assistant outputs may appear in any of these locations:

- `turns` entries with `role: "assistant"`
- `assistant_outputs`
- `model_outputs`
- `responses`
- `transcript`

Each entry can be a plain string or an object containing `content`.

## Output Characteristics

- deterministic for the same input
- JSON-friendly
- useful for before/after mitigation comparison
- intended for MVP-level automated scoring, not final human adjudication

## Summaries

Use `summarize.py` to aggregate score files and optionally compare them:

```bash
python3 evaluators/summarize.py --in reports/scores.json --out-json reports/summary.json --out-md reports/summary.md --pretty
python3 evaluators/summarize.py --in reports/mitigated_scores.json --compare reports/baseline_scores.json --out-json reports/mitigated_summary.json --out-md reports/mitigated_summary.md --pretty
```
