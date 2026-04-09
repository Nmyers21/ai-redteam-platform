# Experiments

This module runs the full red-team MVP in one command:

1. generate deterministic attacks
2. replay them against a model provider
3. evaluate scores
4. emit aggregate summary reports

## Example

```bash
python3 experiments/run_experiment.py --provider mock --count 20 --turns 3 --pretty
```

This writes:

- `reports/raw_attacks.json`
- `reports/model_runs.json`
- `reports/scores.json`
- `reports/summary.json`
- `reports/summary.md`

To compare against a baseline score file:

```bash
python3 experiments/run_experiment.py --provider mock --compare-scores reports/baseline_scores.json --pretty
```
