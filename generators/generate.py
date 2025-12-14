from __future__ import annotations

# --- Imports standard libraries only ---
import argparse
import hashlib
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# --- Constants ---
SCHEMA_VERSION = "v0" 
GENERATOR_VERSION = "0.1.0"

ADVERSARIES = [
    "Casual Policy Tester",
    "Persistent Jailbreaker",
    "Indirect Prompt Injector",
    "Semantic Obfuscator",
]

ATTACK_FAMILIES = [
    "prompt Injection",
    "semantic_obfuscation",
    "multi_turn_escalation",
    "formatting_variance",
]

# Content-agnostic mutation catalog
MUTATION_CATALOG = [
    "structural_reframing",
    "instruction_nesting",
    "contextual_role_confusion",
    "paraphrasing",
    "translation_roundtrip",
    "formatting_variance",
    "token_boundary_manipulation",
]



# --- Data Models
@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    mutation_type: str
    params: Dict[str, Any]
    order: int


@dataclass(frozen=True)
class Turn:
    turn_index: int
    role: str
    content: str
    notes: str = ""


@dataclass(frozen=True)
class AttackCase:
    attack_id: str
    schema_version: str
    seed: int
    created_utc: str

    adversary: str
    attack_family: str

    base_prompt_id: str
    mutations: List[Mutation]
    turns: List[Turn]

    expected_failure_modes: List[str]
    metadata: Dict[str, Any]

    