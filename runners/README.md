# Model Runners

The runner layer replays generated attack cases against a chat model and stores assistant outputs in a format the evaluator can score.

## Supported Providers

- `mock`: deterministic local responses for testing pipelines without API calls
- `openai_compatible`: HTTP calls to `/chat/completions` for OpenAI-compatible endpoints

## Input

Runner input accepts the same case shape produced by `generators/generate.py`:

- a single case object
- or an array of case objects

## Output

Each case is enriched with:

- `assistant_outputs`: list of assistant text replies
- `model_outputs`: structured per-turn replies
- `transcript`: replayed conversation with source annotations
- `model_run`: provider/model configuration and status metadata

## Example

```bash
python3 runners/run_model.py --provider mock --in reports/raw_attacks.json --out reports/model_runs.json --pretty
python3 evaluators/evaluate.py --in reports/model_runs.json --out reports/scores.json --pretty
```

For real model calls:

```bash
export OPENAI_API_KEY="YOUR_KEY"
python3 runners/run_model.py --provider openai_compatible --model gpt-4o-mini --in reports/raw_attacks.json --out reports/model_runs.json --pretty
```
