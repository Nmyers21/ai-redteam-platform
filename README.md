# AI Red Team Platform

Safe-by-design MVP for generating and scoring reproducible LLM red-team cases without publishing harmful payloads.

## What This Project Does

This repository focuses on one narrow problem: building a deterministic, offline workflow for creating adversarial prompt cases and scoring their risk or observed failure signals in a repeatable way.

The current MVP includes:

- deterministic attack-case generation from fixed seeds
- model replay against mock or OpenAI-compatible chat endpoints
- safe, content-agnostic mutation metadata
- a rule-based evaluator that supports both attack-only inputs and response-aware inputs
- aggregate reporting with optional baseline comparison deltas
- one-command experiment orchestration
- documented scope, threat model, and methodology

## What It Does Not Do

This is not yet a production orchestration platform. It does not:

- call model provider APIs directly
- manage experiment queues or dashboards
- claim exhaustive coverage of OWASP LLM Top 10 or MITRE ATLAS
- generate real-world harmful instructions or exploit payloads

## Repository Layout

- `generators/`: deterministic attack-case generation
- `runners/`: model replay and transcript capture
- `evaluators/`: rule-based scoring logic and evaluator docs
- `experiments/`: end-to-end orchestration
- `reports/`: sample generated artifacts
- `scope.md`: in-scope and out-of-scope boundaries
- `threat_model.md`: adversaries, risks, and failure conditions
- `methodology.md`: experimental workflow and scoring design
- `ethics.md`: safety and disclosure constraints

## Quick Start

Run commands from the repository root:

```bash
python3 experiments/run_experiment.py --provider mock --count 20 --turns 3 --pretty
python3 -m unittest discover -s tests
```

To run the steps manually instead of using the one-command experiment script:

```bash
python3 generators/generate.py --seed 1337 --turns 3 --count 5 --created-utc 2026-01-02T15:15:19Z --pretty --out reports/raw_attacks.json
python3 runners/run_model.py --provider mock --in reports/raw_attacks.json --out reports/model_runs.json --pretty
python3 evaluators/evaluate.py --in reports/model_runs.json --out reports/scores.json --pretty
python3 evaluators/summarize.py --in reports/scores.json --out-json reports/summary.json --out-md reports/summary.md --pretty
```

Use `--created-utc` when you want byte-for-byte reproducible generated attack artifacts.

## Input Modes

The evaluator supports two modes:

1. Attack-only mode
   Use raw generator output. The evaluator computes attack surface and persistence risk, but leaves observed failure fields as `null` because no assistant output is present.
2. Response-aware mode
   Provide assistant/model outputs alongside the attack case. The evaluator applies deterministic heuristics to detect likely refusal behavior, instruction-hierarchy confusion, and multi-turn guardrail degradation.

Assistant outputs can be supplied through:

- assistant-role entries inside `turns`
- `assistant_outputs`
- `model_outputs`
- `responses`
- `transcript`

The runner writes both `assistant_outputs` and `transcript`, so the evaluator can score replayed runs without extra conversion.

## Example Output

The evaluator emits one score record per case with fields such as:

- `scoring_mode`
- `attack_surface_score`
- `severity`
- `persistence`
- `policy_violation`
- `guardrail_bypass`
- `evidence`

The summarizer emits:

- aggregate rates and score means
- severity and attack-surface distributions
- top evidence signals
- optional before/after deltas against a baseline score file

## Why This Repo Is Useful

The value of this project is reproducibility. With fixed seeds and deterministic heuristics, you can:

- replay the same attack set before and after a mitigation
- compare runs without manual scoring drift
- document failure modes without distributing unsafe prompt content

## Current Limitations

- runner supports mock and OpenAI-compatible `/chat/completions` endpoints only
- evaluator logic is heuristic, not model-graded
- schemas are documented in Markdown rather than enforced with JSON Schema tooling
- no dashboard UI is included (artifacts are JSON/Markdown files)

## Next Logical Extensions

- add provider adapters beyond OpenAI-compatible chat completions (for example Responses API or local models)
- add richer per-family/per-adversary analytics and plots
- version formal JSON Schemas for generator and evaluator artifacts
