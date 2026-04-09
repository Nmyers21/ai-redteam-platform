from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from experiments.run_experiment import run_pipeline
from runners.run_model import RunnerConfig


class ExperimentTests(unittest.TestCase):
    def test_run_pipeline_generates_all_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            attacks_out = root / "raw_attacks.json"
            runs_out = root / "model_runs.json"
            scores_out = root / "scores.json"
            summary_json_out = root / "summary.json"
            summary_md_out = root / "summary.md"

            result = run_pipeline(
                seed=1337,
                count=3,
                turns=2,
                created_utc="2026-01-02T15:15:19Z",
                config=RunnerConfig(
                    provider="mock",
                    model="mock-model",
                    base_url="mock://local",
                    temperature=0.0,
                    max_tokens=64,
                    timeout_sec=5,
                    system_prompt="You are safe.",
                ),
                attacks_out=attacks_out,
                runs_out=runs_out,
                scores_out=scores_out,
                summary_json_out=summary_json_out,
                summary_md_out=summary_md_out,
                compare_scores_path=None,
                api_key_env="OPENAI_API_KEY",
                sleep_ms=0,
                fail_fast=True,
                pretty=True,
            )

            self.assertEqual(result["cases"], 3)
            self.assertTrue(attacks_out.exists())
            self.assertTrue(runs_out.exists())
            self.assertTrue(scores_out.exists())
            self.assertTrue(summary_json_out.exists())
            self.assertTrue(summary_md_out.exists())

            scores = json.loads(scores_out.read_text(encoding="utf-8"))
            self.assertEqual(len(scores), 3)
            self.assertTrue(all(record.get("scoring_mode") == "response_aware" for record in scores))

            summary_payload = json.loads(summary_json_out.read_text(encoding="utf-8"))
            self.assertEqual(summary_payload["summary"]["total_cases"], 3)


if __name__ == "__main__":
    unittest.main()
