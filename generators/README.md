# Attack Generators

## Purpose
The attack generation layer is responsible for producing structured, reproducible adversarial test cases against a target LLM. Rather than relying on manual prompt crafting, generators systematically create adversarial inputs using deterministic transformations that can be replayed, scaled, and evaluated quantitatively.

This layer does **not** evaluate model responses or apply mitigations. Its sole responsibility is to generate attack inputs.

---

## Inputs
An attack generator accepts the following inputs:

- **Seed**: Integer used to ensure deterministic prompt generation
- **Adversary Class**: The attacker profile being simulated (e.g., Persistent Jailbreaker)
- **Attack Family**: High-level category of attack (e.g., prompt injection, semantic obfuscation)
- **Base Prompt**: A benign or neutral starting prompt used as the mutation source
- **Configuration Parameters**:
  - Number of turns
  - Mutation depth
  - Enabled transformation types

---

## Outputs
Each generator produces a structured JSON object representing a single attack scenario, including:

- Unique attack identifier
- Seed used for generation
- Adversary class
- Attack family
- One or more conversation turns (for multi-turn attacks)
- Metadata required for downstream evaluation

The output format is intentionally model-agnostic and designed for batch execution.

---

## Determinism Requirements
All attack generation must be deterministic:

- Identical inputs and seeds must produce identical outputs
- No non-seeded randomness is permitted
- Any stochastic process must be explicitly controlled

This ensures reproducibility and enables reliable before/after mitigation comparisons.

---

## Design Constraints
- No manual prompt hacking or handcrafted exploit payloads
- No model calls during generation (generation is offline)
- No evaluation or scoring logic in this layer
- Transformations must be content-agnostic and reusable

---

## Extensibility
New attack families or mutation strategies should be added without modifying existing generators. The system is designed to support incremental expansion while preserving backward compatibility and reproducibility.
