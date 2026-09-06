---
name: agent-skill-evolution-workflow
description: 公司级 Agent Skill 生命周期主路由。用于创建、归类、重构、冲突审计、MOE 设计、达尔文迭代、验证交付、GitHub 开源和上游贡献；当任务同时涉及 Skill 与代码时由本入口主持流程，并调用全栈开发原则完成实现。
---

# Skill 迭代与进化

先读取目标 Skill，仅查询 `company-skills.json` 中相关条目；涉及引入、复制或公开发布时核对来源与许可证。一次选择当前需要的专家，专家返回后继续用户已要求且已授权的后续步骤，直到本次交付范围完成；不自动升级为全套发布。

| 当前结果 | 调用 |
|---|---|
| 判断是否需要 Skill、归入哪个部门 | `skill-evolution-intake-classifier` |
| 识别重复、触发冲突和规则矛盾 | `skill-evolution-conflict-auditor` |
| 创建或重构单 Skill/MOE 仓库 | `skill-evolution-project-builder` |
| 根据真实反馈做可回滚迭代 | `skill-evolution-darwin-runner` |
| 验证、安装、同步或按需交付 | `skill-evolution-validation-delivery` |
| 许可、GitHub、公开版本和上游贡献 | `skill-evolution-open-source-upstream` |

## 规则

- 用户明确点名 Skill 时尊重点名；生命周期任务默认由本入口负责。
- 新能力只有在会重复使用且现有 Skill 不覆盖时才创建。
- 用户确认某版满意或要求沉淀时，路由到达尔文迭代；不能把一次反馈直接写进所有 Skill。
- 代码实现遵循 `full-stack-development-workflow` 和 `codex-dev-good-taste`。
- 旧入口保持兼容；平台工具作为外部依赖，不搬进部门仓库。
- 未确认许可的第三方内容只引用，不复制进公开仓库。
- 外部发布、批量覆盖和生产同步核对明确授权、备份和回读；已有具体授权继续有效，不因换专家再次批准。本地审计与修复不强制 GitHub、云端同步、ZIP 或教程。

