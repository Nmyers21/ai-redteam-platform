## System Overview

This project evaluates the security and safety robustness of a target LLM by running automated, reproducible adversarial test cases against it. Untrusted input enters through user prompts (single-turn and multi-turn conversations) and is transformed by an attack generation layer (mutations, paraphrasing, encoding, multilingual variants) into candidate adversarial prompts. The platform sends these prompts to the model under test (and optionally a defended/mitigated configuration), collects model outputs, and scores them using an automated evaluator that produces structured metrics (e.g., violation rate, severity, persistence across turns). The system’s core trust boundary is between untrusted user-controlled text and the model/system instructions; the primary assets are policy compliance, instruction hierarchy integrity, and prevention of unsafe or disallowed outputs. Outputs and results are stored as JSON/CSV (and summarized into a report) with deterministic seeds and version-locked dependencies to enable one-command replays and before/after mitigation comparisons.
## Adversary Classes

### Adversary: Casual Policy Tester

**Goal:**  
Elicit disallowed or policy-restricted behavior from the model through simple or naïve probing.

**Capabilities:**  
- Submits arbitrary single-turn prompts  
- Attempts basic rephrasing or clarification requests  
- Observes refusals and adjusts wording slightly  

**Constraints:**  
- No access to system or developer prompts  
- Limited persistence across turns  
- No intent to deeply obfuscate or escalate  

**Primary Risks Introduced:**  
- Surface-level policy violations  
- Overly permissive responses to poorly framed safety rules  
- Inconsistent enforcement across similar prompts  
**OWASP LLM Top 10 Mapping:**  
- LLM01: Prompt Injection  
- LLM07: Insecure Model Output Handling  

**MITRE ATLAS Techniques:**  
- Prompt Manipulation  
- Policy Evasion via Simple Rephrasing  


---

### Adversary: Persistent Jailbreaker

**Goal:**  
Gradually bypass safety controls by exploiting multi-turn context and conversational drift.

**Capabilities:**  
- Maintains multi-turn conversations  
- Uses incremental escalation and reframing  
- Exploits memory and context accumulation  

**Constraints:**  
- No direct modification of system instructions  
- Cannot execute external code or tools  
- Operates entirely within conversational input  

**Primary Risks Introduced:**  
- Delayed policy violations after benign setup  
- Safety degradation over time  
- Context-based override of initial guardrails  
**OWASP LLM Top 10 Mapping:**  
- LLM01: Prompt Injection  
- LLM05: Improper Handling of Model Context  
- LLM06: Overreliance on LLM Outputs  

**MITRE ATLAS Techniques:**  
- Context Poisoning  
- Multi-Turn Instruction Manipulation  


---

### Adversary: Indirect Prompt Injector

**Goal:**  
Influence model behavior by embedding adversarial instructions within otherwise legitimate content.

**Capabilities:**  
- Injects instructions into quoted text, summaries, or user-provided data  
- Exploits instruction hierarchy ambiguity  
- Leverages task confusion (e.g., “summarize” vs “follow”)  

**Constraints:**  
- No direct access to system or tool configuration  
- Cannot alter model parameters  
- Limited to text-based injection  

**Primary Risks Introduced:**  
- Instruction-following confusion  
- Untrusted content overriding developer intent  
- Leakage of system behavior or assumptions  
**OWASP LLM Top 10 Mapping:**  
- LLM01: Prompt Injection  
- LLM02: Insecure Data Handling  

**MITRE ATLAS Techniques:**  
- Indirect Prompt Injection  
- Instruction Hierarchy Confusion  


---

### Adversary: Semantic Obfuscator

**Goal:**  
Bypass safety filters by expressing disallowed intent through paraphrasing, encoding, or indirection.

**Capabilities:**  
- Uses paraphrasing and semantic rewording  
- Employs translation or encoding to mask intent  
- Avoids obvious keywords or patterns  

**Constraints:**  
- No access to internal model representations  
- Cannot change evaluation logic directly  
- Relies solely on input phrasing  

**Primary Risks Introduced:**  
- Failure of keyword- or pattern-based filters  
- Inconsistent policy enforcement across languages or encodings  
- Undetected policy violations due to semantic ambiguity  
**OWASP LLM Top 10 Mapping:**  
- LLM01: Prompt Injection  
- LLM04: Model Denial of Service (via filter evasion loops)  

**MITRE ATLAS Techniques:**  
- Semantic Evasion  
- Encoding and Translation-Based Obfuscation  
## Failure Conditions

- The model produces policy-violating content as determined by the automated evaluator
- A violation occurs after a benign initial prompt through multi-turn escalation
- The model follows adversarial instructions embedded in untrusted content
- The model’s safety posture degrades across turns (increased compliance over time)
- The same failure is reproducible under identical seeds and model versions

