# Agent Skill Evolution Workflow

公司级 Skill 生命周期 MOE：归类、冲突审计、项目构建、达尔文迭代、验证交付和开源上游贡献。

```bash
python3 tools/build_inventory.py --cloud-list /tmp/cloud-skills.txt
python3 tools/validate_project.py .
python3 -m unittest discover -s tests -v
node tools/install.mjs
```

`company-skills.json` 是四个部门入口、专家、共享工具、外部依赖和旧入口的登记表。
Company-level MOE Agent Skill for classification, conflict auditing, creation, evolution, delivery, and upstream contribution.
