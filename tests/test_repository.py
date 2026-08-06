from __future__ import annotations

import json
import subprocess
import tempfile
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
        valid_roles = {"部门入口", "部门专家", "共享工具", "外部依赖", "旧入口"}
        valid_departments = {"full-stack-development", "social-media-operations", "course-production", "skill-evolution", None}
        for item in registry["skills"]:
            self.assertIn(item["role"], valid_roles)
            self.assertIn(item["department"], valid_departments)
            if item["role"] == "旧入口":
                self.assertEqual(item["legacy_compatibility"]["status"], "preserved")
        self.assertEqual(len(registry["skills"]), len({item["machine_name"] for item in registry["skills"]}))
        versions = {item["machine_name"]: item["install_version"] for item in registry["skills"]}
        self.assertEqual(versions["full-stack-development-workflow"], "2.0.0")
        self.assertEqual(versions["social-media-creator-workflow"], "1.3.0")
        self.assertEqual(versions["agent-skill-evolution-workflow"], "1.1.0")
        self.assertEqual(versions["skill-evolution-validation-delivery"], "1.1.0")
        self.assertEqual(versions["course-producer"], "1.1.0")
        self.assertEqual(versions["course-lark-delivery"], "1.1.0")
        self.assertEqual(versions["course-quality-editor"], "1.1.0")

    def test_delivery_expert_uses_one_four_stage_receipt(self) -> None:
        text = (ROOT / "skills" / "skill-evolution-validation-delivery" / "SKILL.md").read_text(encoding="utf-8")
        for expected in (
            ".skill-delivery-receipt.json",
            "## 1. 本地候选",
            "## 2. GitHub 基线",
            "## 3. Zeabur 原子同步",
            "## 4. 中央登记与收口",
            "local/github/cloud/registry",
        ):
            self.assertIn(expected, text)

    def test_inventory_preserves_curated_metadata(self) -> None:
        source = json.loads((ROOT / "company-skills.json").read_text(encoding="utf-8"))
        item = next(x for x in source["skills"] if x["machine_name"] == "job-resume-intelligent-matching-fanhan")
        self.assertEqual(item["install_version"], "2.1.0")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "company-skills.json"
            output.write_text(json.dumps({"skills": [item]}, ensure_ascii=False), encoding="utf-8")
            subprocess.run(
                ["python3", str(ROOT / "tools" / "build_inventory.py"), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            rebuilt = json.loads(output.read_text(encoding="utf-8"))
            preserved = next(
                x for x in rebuilt["skills"] if x["machine_name"] == "job-resume-intelligent-matching-fanhan"
            )
            self.assertEqual(preserved["install_version"], "2.1.0")


if __name__ == "__main__":
    unittest.main()
