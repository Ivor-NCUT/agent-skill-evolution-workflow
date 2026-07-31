---
name: skill-evolution-validation-delivery
description: 验证、安装和同步 Agent Skill，并在用户明确要求时完成压缩包、教程或飞书交付。用于 Skill 创建或迭代完成后的 quick_validate、仓库测试、本地与云端版本一致性、兼容检查和系统提示更新。
---

# Skill 验证交付

1. 运行每个 Skill 的 `quick_validate.py` 和仓库测试。
2. 校验来源、许可证、路由用例、旧入口和公共路径。
3. 安装器只能管理自己的符号链接；真实目录先备份，不静默覆盖。
4. 本地与云端比较入口 Skill、`project.json` 和登记版本的 SHA-256。
5. 用户要求 ZIP、教程或飞书交付时调用 `skill-delivery-workflow`；未要求则不扩张交付物。
6. 回读全局路由和生产健康后才报告完成。

失败时保留备份和证据，禁止用“命令成功”代替真实验收。

