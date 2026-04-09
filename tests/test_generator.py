from __future__ import annotations

import unittest
from dataclasses import asdict

from generators.generate import generate_one


class GeneratorTests(unittest.TestCase):
    def test_generate_one_is_deterministic_for_same_seed(self) -> None:
        first = asdict(generate_one(seed=1337, turns=3))
        second = asdict(generate_one(seed=1337, turns=3))

        self.assertEqual(first["attack_id"], second["attack_id"])
        self.assertEqual(first["adversary"], second["adversary"])
        self.assertEqual(first["attack_family"], second["attack_family"])
        self.assertEqual(first["mutations"], second["mutations"])
        self.assertEqual(first["turns"], second["turns"])

    def test_generate_one_changes_with_seed(self) -> None:
        first = asdict(generate_one(seed=1337, turns=3))
        second = asdict(generate_one(seed=1338, turns=3))

        self.assertNotEqual(first["attack_id"], second["attack_id"])


if __name__ == "__main__":
    unittest.main()
