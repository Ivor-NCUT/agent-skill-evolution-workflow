# Repository rules

- Keep the lifecycle router thin and preserve standalone Skill compatibility.
- Treat `company-skills.json` as the registry of installed and managed capabilities.
- Do not copy third-party content without a redistribution-compatible license.
- Update routing cases when behavior changes; update architecture and project metadata when structure or release metadata changes. Update registry entries only when installation or publication facts change, preserving existing user edits. Pure instruction fixes do not require a new version or publication.
- Run the project validator, unit tests, and `quick_validate.py` for each changed Skill.
