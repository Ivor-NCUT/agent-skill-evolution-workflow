#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
project = json.loads((root / "project.json").read_text(encoding="utf-8"))
registry = json.loads((root / "company-skills.json").read_text(encoding="utf-8"))
errors: list[str] = []
for name in ("README.md", "AGENTS.md", "LICENSE", "VERSION", "project.json", "company-skills.json"):
    if not (root / name).is_file():
        errors.append(f"missing {name}")
names = [project["entry_skill"], *[item["skill"] for item in project["experts"]]]
for name in names:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append(f"invalid skill name: {name}")
    path = root / "skills" / name / "SKILL.md"
    if not path.is_file() or "[TODO" in path.read_text(encoding="utf-8"):
        errors.append(f"invalid skill: {name}")
if len(registry.get("departments", [])) != 4:
    errors.append("registry must contain four departments")
if errors:
    print("INVALID")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)
print(f"VALID: {root}")
