# Architecture

主路由根据当前生命周期结果选择一个专家。`company-skills.json` 记录四个部门、安装来源和兼容关系；它不是复制全部 Skill 内容的仓库。

平台连接器保持共享工具。全栈开发负责代码质量，社媒运营负责开源宣发，课程制作人保持独立业务边界。本仓库负责 Skill 自身的治理与变更流程。

Agent 文档设计规则集中在主路由的 `references/agent-document-design.md`。只有构建、
冲突审计或验证涉及 Skill 与 Agent 指令文档时才读取；三个专家共享同一事实源，不在
各自流程中复制规则。

验证交付专家使用单一 `.skill-delivery-receipt.json` 串联本地候选、GitHub 默认分支、
Zeabur 原子同步和 `company-skills.json` 登记。四段共享版本、commit/tree、SHA、验证与
回滚证据；任何阶段失败都停在该阶段，不能由后续阶段的“成功”覆盖。
