# Scope

## In-scope
- Programmatic generation of adversarial prompts against LLMs (non-harmful content only)
- Prompt injection, policy evasion, and multi-turn persistence testing
- Evaluation of guardrail failures using objective, reproducible metrics
- Validation of mitigations such as prompt hardening and input/output filtering

## Out-of-scope
- Malware, exploits, weapons, fraud, or instructions enabling real-world harm
- Attacks against real third-party systems or services without authorization
- Collection, use, or storage of real personal or sensitive data
- Social engineering of real users or attempts to bypass non-LLM security controls

## Assumptions
- Target models may hallucinate or behave nondeterministically
- Automated evaluators may produce false positives or false negatives
- Safety policies differ across model providers and versions

## Safety Controls
- Use only synthetic prompts and generated outputs
- Run experiments locally or in isolated, rate-limited environments
- Log and review outputs to prevent accidental harmful content inclusion

## Success Criteria
- Deterministic, repeatable attack runs with fixed seeds and versioned models
- Quantitative metrics showing attack success and mitigation effectiveness
- Clear documentation of limits, risks, and ethical boundaries
