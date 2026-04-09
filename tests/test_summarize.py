from __future__ import annotations

import unittest

from evaluators.summarize import compare_summaries, summarize_scores


class SummarizeTests(unittest.TestCase):
    def test_summarize_scores_computes_expected_rates(self) -> None:
        scores = [
            {
                "attack_id": "a1",
                "scoring_mode": "response_aware",
                "attack_surface_score": 5,
                "severity": 2,
                "turn_count": 3,
                "policy_violation": 1,
                "guardrail_bypass": 1,
                "persistence": 1,
                "evidence": ["x", "y"],
            },
            {
                "attack_id": "a2",
                "scoring_mode": "response_aware",
                "attack_surface_score": 3,
                "severity": 1,
                "turn_count": 2,
                "policy_violation": 0,
                "guardrail_bypass": 0,
                "persistence": 0,
                "evidence": ["x"],
            },
            {
                "attack_id": "a3",
                "scoring_mode": "attack_only",
                "attack_surface_score": 7,
                "severity": 2,
                "turn_count": 4,
                "policy_violation": None,
                "guardrail_bypass": None,
                "persistence": 1,
                "evidence": ["z"],
            },
        ]

        summary = summarize_scores(scores)

        self.assertEqual(summary["total_cases"], 3)
        self.assertEqual(summary["mode_counts"]["response_aware"], 2)
        self.assertAlmostEqual(summary["policy_violation_rate"], 0.5)
        self.assertAlmostEqual(summary["guardrail_bypass_rate"], 0.5)
        self.assertAlmostEqual(summary["persistence_rate"], 2 / 3)
        self.assertEqual(summary["severity_distribution"]["1"], 1)
        self.assertEqual(summary["severity_distribution"]["2"], 2)

    def test_compare_summaries_returns_metric_deltas(self) -> None:
        baseline = {
            "avg_attack_surface_score": 5.0,
            "avg_severity": 2.0,
            "avg_turn_count": 3.0,
            "policy_violation_rate": 0.40,
            "guardrail_bypass_rate": 0.50,
            "persistence_rate": 0.70,
        }
        candidate = {
            "avg_attack_surface_score": 4.5,
            "avg_severity": 1.5,
            "avg_turn_count": 3.2,
            "policy_violation_rate": 0.20,
            "guardrail_bypass_rate": 0.30,
            "persistence_rate": 0.60,
        }

        delta = compare_summaries(baseline, candidate)

        self.assertAlmostEqual(delta["avg_attack_surface_score"], -0.5)
        self.assertAlmostEqual(delta["avg_severity"], -0.5)
        self.assertAlmostEqual(delta["avg_turn_count"], 0.2)
        self.assertAlmostEqual(delta["policy_violation_rate"], -0.2)
        self.assertAlmostEqual(delta["guardrail_bypass_rate"], -0.2)
        self.assertAlmostEqual(delta["persistence_rate"], -0.1)


if __name__ == "__main__":
    unittest.main()
