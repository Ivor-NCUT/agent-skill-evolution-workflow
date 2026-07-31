---
name: skill-evolution-project-builder
description: 创建或重构单 Agent Skill 与路由加专家的 MOE 仓库。用于用户已明确目标、触发场景和交付边界的 Skill 开发任务；使用官方 Skill Creator 或 MOE Skill Creator，按 GitHub Issue 最小实现并维护来源、许可、架构和测试。
---

# Skill 项目构建

1. 先读真实材料、现有仓库、目标运行时和许可。
2. 单 Skill 使用官方 `skill-creator` 初始化；MOE 使用 `moe-skill-creator` 的架构与验证器。
3. 父路由保持薄，专家各自拥有一个可检查输出，知识按需加载。
4. 使用 `full-stack-development-workflow` 按 Issue 实现；不新增不必要依赖。
5. 每个新 Skill 运行 `quick_validate.py`，仓库运行最小路由测试。

用户指定独立仓库时不要同时发布到合集仓库。

