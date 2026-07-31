---
name: skill-evolution-open-source-upstream
description: 处理 Agent Skill 的许可证、GitHub 版本、公开发布和第三方上游贡献。用于新建公开仓库、发布原创 Skill、采用外部 Skill、修改第三方能力或需要 Issue/PR；先审计权利和查重，再通过 GitHub CLI 留下可回读记录。
---

# Skill 开源与上游贡献

1. 区分原创、用户私有材料、MIT/Apache 等可改编内容和无许可内容。
2. 原创公开版本默认使用已确认许可证；无许可内容只引用架构，不复制。
3. GitHub 远端操作使用 `gh/gh api`，先查重再建 Issue 或 PR。
4. 可复用的第三方修复优先上游 PR；部署侧经验至少关联脱敏 Issue。
5. 禁止提交密钥、用户数据、私聊、私有日志和仅属于内部业务的代码。
6. 开源宣发交给社媒仓库的 `open-source-launch` 专家，本专家不自动发帖。
