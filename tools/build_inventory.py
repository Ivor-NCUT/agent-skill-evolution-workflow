#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEPARTMENTS = {
    "full-stack-development": {
        "entry": "full-stack-development-workflow",
        "repo": "Ivor-NCUT/full-stack-development-workflow",
        "prefixes": ("full-stack-",),
    },
    "social-media-operations": {
        "entry": "social-media-creator-workflow",
        "repo": "Ivor-NCUT/social-media-creator-workflow",
        "prefixes": ("social-media-creator-workflow-",),
    },
    "course-production": {
        "entry": "course-producer",
        "repo": "Ivor-NCUT/course-producer",
        "prefixes": ("course-",),
    },
    "skill-evolution": {
        "entry": "agent-skill-evolution-workflow",
        "repo": "Ivor-NCUT/agent-skill-evolution-workflow",
        "prefixes": ("skill-evolution-",),
    },
}

LEGACY_PATTERNS = {
    "full-stack-development": re.compile(r"(codex-dev|webapp|vercel-react|gh-fix|gh-address|insforge)"),
    "social-media-operations": re.compile(r"(content|writing|xhs|小红书|招聘广告|公众号|标题|视频号|agent-reach|口播|粗剪)"),
    "course-production": re.compile(r"(course|课程|培训讲解)"),
    "skill-evolution": re.compile(r"(skill-creator|skill-delivery|skill-github|skill-迭代|达尔文|moe-skill)"),
}


def skill_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
    return match.group(1).strip() if match else path.parent.name


def classify(name: str) -> tuple[str | None, str]:
    for department, spec in DEPARTMENTS.items():
        if name == spec["entry"]:
            return department, "department-entry"
        if any(name.startswith(prefix) for prefix in spec["prefixes"]):
            return department, "department-expert"
    if name in {"agent-reach", "ponytail", "moe-skill-creator"}:
        return None, "external-dependency"
    for department, pattern in LEGACY_PATTERNS.items():
        if pattern.search(name.lower()):
            return department, "legacy-entry"
    return None, "shared-tool"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cloud-list", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[1] / "company-skills.json")
    args = parser.parse_args()
    discovered: dict[str, dict] = {}
    workspace = Path(__file__).parents[2]
    roots = [
        Path.home() / ".agents/skills",
        Path.home() / ".codex/skills",
        *[workspace / spec["repo"].split("/", 1)[1] / "skills" for spec in DEPARTMENTS.values()],
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("SKILL.md"):
            if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
                continue
            name = skill_name(path)
            discovered.setdefault(name, {"local_paths": [], "cloud": False})["local_paths"].append(str(path.parent))
    if args.cloud_list and args.cloud_list.exists():
        for name in args.cloud_list.read_text(encoding="utf-8").splitlines():
            if name.strip():
                discovered.setdefault(name.strip(), {"local_paths": [], "cloud": False})["cloud"] = True
    skills = []
    for name, found in sorted(discovered.items()):
        department, role = classify(name)
        spec = DEPARTMENTS.get(department)
        skills.append({
            "machine_name": name,
            "source": {"local_paths": sorted(set(found["local_paths"])), "cloud_installed": found["cloud"]},
            "department": department,
            "role": role,
            "github_repository": spec["repo"] if role in {"department-entry", "department-expert"} and spec else None,
            "install_version": "1.0.0" if role in {"department-entry", "department-expert"} and spec else None,
            "license": "MIT" if role in {"department-entry", "department-expert"} and spec else "unknown",
            "legacy_aliases": [],
        })
    payload = {
        "schema_version": 1,
        "departments": [
            {"id": key, "entry_skill": value["entry"], "github_repository": value["repo"]}
            for key, value in DEPARTMENTS.items()
        ],
        "skills": skills,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(skills)} skills to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
