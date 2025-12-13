# Ethics Statement

## Purpose
This project exists to improve the safety, robustness, and trustworthiness of large language models by identifying and mitigating systemic weaknesses through ethical red teaming.

## Ethical Principles
- Safety-first: prioritize harm prevention over exploit demonstration
- Least harm: avoid generating or amplifying dangerous content
- Transparency: clearly document methods, limits, and assumptions
- Accountability: ensure results are reproducible and auditable

## Data Handling
- Use only synthetic prompts and model-generated outputs
- Do not collect, store, or process real personal or sensitive data
- No logging of user-identifiable information

## Testing Environment
- Conduct testing only in controlled, isolated environments
- Respect model provider terms of service and usage policies
- Apply rate limits and safeguards to prevent abuse or runaway generation

## Abuse Prevention
- Exclude prompts that meaningfully enable wrongdoing (e.g., violence, malware, fraud)
- Avoid publishing step-by-step harmful instructions or exploit playbooks
- Frame findings around failure modes and mitigations, not exploitation

## Responsible Disclosure
- If testing public or third-party models, follow responsible disclosure practices
- Share findings in a manner that supports safety improvements, not misuse

## Limitations
- This project does not claim comprehensive coverage of all LLM risks
- Findings are context- and model-dependent and may not generalize universally
