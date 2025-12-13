# Mutation Strategies

## Purpose
Mutation strategies define deterministic transformations applied to benign base prompts in order to systematically explore failure modes in LLM safety and instruction-following. These strategies operate on structure, semantics, and context—not on harmful content or handcrafted payloads.

Mutations are reusable, composable, and adversary-agnostic.

---

## General Rules
- Mutations must be deterministic when provided the same seed
- Mutations must not introduce new intent beyond the base prompt
- Mutations operate on *form*, *structure*, or *context*, not explicit content
- Multiple mutations may be chained to increase attack depth

---

## Prompt Injection Family

### Structural Reframing
- Reorder clauses or sentences without changing semantic meaning
- Change declarative phrasing to instructional phrasing (and vice versa)
- Embed the prompt within a larger benign task description

### Instruction Nesting
- Wrap the base prompt inside quoted, summarized, or referenced text
- Present instructions as part of user-provided data rather than direct input
- Shift instruction boundaries to test hierarchy confusion

### Contextual Role Confusion
- Recast the prompt as an example, hypothetical, or analysis request
- Change implied speaker or role without altering surface content
- Introduce ambiguity about whether text should be followed or examined

---

## Semantic Obfuscation Family

### Paraphrasing
- Rewrite prompts using synonymous language
- Alter sentence structure while preserving intent
- Simplify or expand phrasing without semantic drift

### Indirection
- Replace direct requests with implied or descriptive language
- Frame intent through outcomes rather than instructions
- Use abstract references instead of explicit directives

### Translation-Based Transformation
- Translate prompt to another language and back
- Mix languages within a single prompt
- Preserve meaning while altering surface tokens

---

## Multi-Turn Escalation

### Incremental Context Build-Up
- Split a single request across multiple turns
- Introduce information gradually instead of all at once
- Delay the critical transformation until later turns

### Context
