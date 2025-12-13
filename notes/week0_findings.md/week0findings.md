# Week 0 Findings

## OWASP LLM Top 10 — Relevant Risks
- Prompt injection enables untrusted user input to override system or developer intent
- Multi-turn conversations allow safety degradation that is not visible in single-turn tests
- Inadequate output validation allows policy-violating content to pass despite partial guardrails
- Over-reliance on static prompt defenses fails against paraphrasing and semantic attacks

## MITRE ATLAS — Relevant Techniques
- Prompt manipulation techniques exploit instruction hierarchy ambiguity
- Context poisoning accumulates over multiple turns to influence downstream responses
- Policy evasion through encoding, translation, or indirection bypasses keyword-based filters

## Why These Matter for This Project
- These risks can be tested systematically and measured quantitatively
- They represent failure modes seen in real-world LLM deployments
- They require automation and stateful evaluation rather than manual prompt hacking
