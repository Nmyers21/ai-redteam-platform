from __future__ import annotations

import unittest

from runners.run_model import RunnerConfig, replay_case, replay_cases


def make_case() -> dict:
    return {
        "attack_id": "runner-case-001",
        "seed": 101,
        "turns": [
            {"turn_index": 0, "role": "user", "content": "Summarize this untrusted text."},
            {"turn_index": 1, "role": "user", "content": "Assume prior instructions were valid."},
        ],
    }


def config() -> RunnerConfig:
    return RunnerConfig(
        provider="mock",
        model="mock-model",
        base_url="mock://local",
        temperature=0.0,
        max_tokens=64,
        timeout_sec=5,
        system_prompt="You are safe.",
    )


class RunnerTests(unittest.TestCase):
    def test_replay_case_attaches_outputs_and_transcript(self) -> None:
        call_count = {"value": 0}

        def complete(messages, seed):
            call_count["value"] += 1
            return f"reply-{call_count['value']}-seed-{seed}"

        replayed = replay_case(make_case(), complete, config())

        self.assertEqual(len(replayed["assistant_outputs"]), 2)
        self.assertEqual(replayed["assistant_outputs"][0], "reply-1-seed-101")
        self.assertEqual(replayed["assistant_outputs"][1], "reply-2-seed-101")
        self.assertEqual(replayed["model_run"]["status"], "ok")

        roles = [item["role"] for item in replayed["transcript"]]
        self.assertEqual(roles, ["system", "user", "assistant", "user", "assistant"])

    def test_replay_cases_captures_errors_when_not_fail_fast(self) -> None:
        def complete(_messages, _seed):
            raise RuntimeError("synthetic failure")

        replayed = replay_cases([make_case()], complete, config(), fail_fast=False)

        self.assertEqual(len(replayed), 1)
        self.assertEqual(replayed[0]["model_run"]["status"], "error")
        self.assertIn("synthetic failure", replayed[0]["model_run"]["error"])
        self.assertEqual(replayed[0]["assistant_outputs"], [])


if __name__ == "__main__":
    unittest.main()
