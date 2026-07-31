from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROJECT = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))


class RepositoryTest(unittest.TestCase):
    def test_skills_and_routes(self) -> None:
        names = [PROJECT["entry_skill"], *[item["skill"] for item in PROJECT["experts"]]]
        for name in names:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)
            self.assertNotIn("[TODO", text)
        cases = json.loads((ROOT / "tests" / "routing_cases.json").read_text(encoding="utf-8"))
        self.assertEqual({case["expected"] for case in cases}, set(names[1:]))

    def test_registry_roles_and_departments(self) -> None:
        registry = json.loads((ROOT / "company-skills.json").read_text(encoding="utf-8"))
        valid_roles = {"department-entry", "department-expert", "shared-tool", "external-dependency", "legacy-entry"}
        valid_departments = {"full-stack-development", "social-media-operations", "course-production", "skill-evolution", None}
        for item in registry["skills"]:
            self.assertIn(item["role"], valid_roles)
            self.assertIn(item["department"], valid_departments)
        self.assertEqual(len(registry["skills"]), len({item["machine_name"] for item in registry["skills"]}))


if __name__ == "__main__":
    unittest.main()
