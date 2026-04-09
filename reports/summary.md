# Evaluation Summary

- generated_utc: 2026-03-04T22:10:15Z
- total_cases: 20
- scoring_modes: {'response_aware': 20}

## Core Metrics

- avg_attack_surface_score: 5.70
- avg_severity: 1.95
- avg_turn_count: 3.00
- policy_violation_rate: 0.0%
- guardrail_bypass_rate: 0.0%
- persistence_rate: 100.0%

## Distributions

- severity_distribution: {'1': 1, '2': 19}
- attack_surface_distribution: {'4': 1, '5': 8, '6': 7, '7': 4}

## Top Evidence Signals

- failure_mode:instruction_hierarchy_confusion: 20
- turn_count>=3: 20
- assistant_refusal_language: 20
- direct_operationalization: 20
- analysis_or_summary_language: 20
- mutation:translation_roundtrip: 10
- attack_family:semantic_obfuscation: 7
- adversary:Indirect Prompt Injector: 7
- mutation:token_boundary_manipulation: 7
- mutation:instruction_nesting: 7
