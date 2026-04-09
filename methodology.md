# Methodology

## Objective

Measure whether a target LLM resists prompt injection, semantic obfuscation, and multi-turn escalation under reproducible conditions.

## Experimental Design

The workflow is intentionally simple:

1. Generate deterministic attack cases from a fixed seed.
2. Replay those cases against a baseline model or defended configuration.
3. Capture assistant outputs and transcript metadata in a structured artifact.
4. Score each case with a deterministic evaluator.
5. Summarize aggregate metrics and compare baseline and mitigated runs under identical seeds.

## Reproducibility Rules

- seeds must be fixed and recorded
- artifact timestamps should be pinned with `--created-utc` when byte-for-byte reproducibility matters
- input cases must remain unchanged between baseline and mitigation runs
- model/version metadata should be logged with every scored run
- evaluator logic must be deterministic and auditable

## Attack Generation Strategy

The generator does not create harmful payloads. Instead, it composes safe, content-agnostic attack structures that stress:

- instruction hierarchy confusion
- indirect prompt following
- context accumulation across turns
- resilience to structural or semantic rewriting

Attack strength is varied by adversary class, attack family, mutation mix, and turn count.

## Evaluation Strategy

The evaluator operates in two distinct modes.

### Attack-Only Mode

If no assistant output is present, the evaluator estimates attack pressure from:

- adversary class
- attack family
- mutation types
- turn count
- expected failure modes

This mode is useful for triage, corpus balancing, and experiment planning. It does not claim that a policy failure was observed.

### Response-Aware Mode

If assistant output is present, the evaluator applies rule-based heuristics to detect:

- refusal or boundary-setting language
- procedural compliance with embedded instructions
- instruction-hierarchy confusion
- multi-turn persistence or degradation

In this mode:

- `policy_violation` reflects likely unsafe operationalization
- `guardrail_bypass` reflects likely instruction-following failure despite a red-team pattern
- `severity` reflects the concentration of risky signals
- `persistence` reflects escalation or repeated risky compliance across turns

## Execution Layer

Use `runners/run_model.py` to replay each user turn against a model and capture:

- per-turn assistant outputs
- full replay transcript
- model/provider metadata needed for run traceability

The runner currently supports deterministic local `mock` responses and `openai_compatible` HTTP chat-completions endpoints.

## Reporting Layer

Use `evaluators/summarize.py` to produce:

- machine-readable aggregate metrics (`summary.json`)
- human-readable experiment readout (`summary.md`)
- optional baseline deltas using `--compare`

## Why Rule-Based Scoring

Rule-based scoring is deliberately limited, but it has two advantages for an MVP:

- the logic is transparent and easy to audit
- results are reproducible across runs without depending on another model

## Threats to Validity

- heuristic scoring can miss subtle failures or misclassify safe explanations
- absence of assistant outputs prevents true failure measurement
- template-based attacks do not cover the full diversity of real user behavior
- different providers may enforce policies differently even for the same prompt set

## Safe Research Boundaries

- use synthetic prompts and generated outputs only
- avoid step-by-step harmful payloads
- do not test third-party systems without authorization
- present findings as failure modes and mitigations, not exploit recipes
