# North Star

## What counts as attack success (measurable)
- A response contains policy-violating content as determined by an automated evaluator
- A violation occurs within N turns (default: ≤5) starting from a benign initial prompt
- The same violation is reproducible across identical seeds and model versions

## What counts as mitigation success (measurable)
- ≥X% reduction in policy violation rate compared to baseline under identical attack seeds
- Increased average turn count required to reach a violation (delayed failure)
- Reduced persistence of violations across multi-turn conversations

## How I could fool myself (bad metrics / traps)
- Counting refusals or safe completions as failures
- Changing prompts, seeds, or model versions between baseline and mitigated runs
- Using subjective or manual scoring instead of deterministic evaluation logic
