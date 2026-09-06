---
name: skill-evolution-validation-delivery
description: 验证、安装和同步 Agent Skill，并在用户明确要求时完成压缩包、教程或飞书交付。用于 Skill 创建或迭代完成后的 quick_validate、仓库测试、本地与云端版本一致性、兼容检查和系统提示更新。
---

# Skill 验证交付

先确定本次交付范围。仅本地修复时，验证与差异记录即可；涉及多端同步时才维护一张
`.skill-delivery-receipt.json`，只执行已请求的阶段，未请求阶段标为 `not_requested`。
不要为本地、GitHub、Zeabur 和登记表分别发明状态，也不因四段模板自动发布。

## 1. 本地候选

1. 记录仓库、版本、基线 commit、用户原有未提交改动和本轮目标文件。
2. 运行每个变更 Skill 的 `quick_validate.py`、仓库 validator、测试和路由用例。
3. 修改了 Skill 或 Agent 文档时，读取
   [Agent 文档设计](../agent-skill-evolution-workflow/references/agent-document-design.md)，
   检查触发分支、信息层级、可检查完成标准、单一事实源和无效指令。
4. 校验来源、许可证、旧入口和公共路径；安装器只能管理自己的符号链接，真实目录
   先备份，不静默覆盖。
5. 需要收据时，只记录实际存在的 `local.commit`、`local.version`、入口 Skill、
   `project.json` 或制品 SHA-256，以及验证结果；无仓库／版本／制品时不为补字段制造它们。检查失败先修复并重跑相关检查，通过前不发布；无法修复则报告准确缺项，不把一次失败当作整个任务结束。

## 2. GitHub 基线

仅在已请求并授权 GitHub 发布／同步时执行。

1. GitHub 远端只使用 `gh` / `gh api`。需要 Issue/PR 时先查重，按请求与仓库流程
   准备目标；不得把用户已有改动误当成本轮内容，不强制每次同步创建全套管理材料。
2. EOF 或超时后先回读 ref、PR、commit/tree SHA，只补缺失动作。
3. 用户只要 PR 时，回读 PR head、目标文件和检查状态即完成该范围；只有明确授权
   合并且必要检查通过时才合并，再回读默认分支 commit/tree。对照实际请求的目标
   记录 `github.commit`、`github.tree`、Issue/PR 与 CI 结果，不把 PR 创建扩张成合并。

## 3. Zeabur 原子同步

仅在已请求并授权该云端目标时执行。

1. 先用 Zeabur Skill 解析精确 project/service/environment，回读当前版本、安装路径、
   运行进程和健康；不要凭旧记忆覆盖。
2. 制品先完整归档并计算 SHA，再上传到新暂存目录。CLI 不转发本地 stdin 时使用
   Base64 分片并逐片回读累计字节；解包后用容器现有运行时验证 JSON、入口和 SHA。
3. 验证通过才执行“备份旧目录 -> 原子切换”。EOF 后回读目标版本、备份和 SHA，
   已切换则不重试。活跃任务默认不重启；只有运行时必须加载新版本且安全时才受控重启。
4. 回读入口 Skill、`project.json`、版本、三个 SHA 和生产健康，写入 `cloud` 与回滚路径。

## 4. 中央登记与收口

1. 安装或发布状态实际变化且需要登记时，用现有 inventory 生成器更新
   `company-skills.json`；先预览 diff，只接受本任务涉及的条目并保留用户原有变更。
   不为纯本地文字修复编造已发布版本或覆盖登记表。
2. 需要登记发布／云端同步且已授权时，按对应流程执行并保留备份。回读所有受影响
   条目的版本与安装状态，写入 `registry`。
3. 若请求完整四方同步，核对 `local/github/cloud/registry` 对应版本与制品 SHA、CI
   和生产健康；单端交付只验该端。未请求云端标 `not_requested`，已请求但无法完成标
   `blocked`，两者不可混用，不得用本地成功冒充四方完成。

收据只存提交、版本、SHA、链接、验证和回滚路径，不存 token、secret 或私有日志。
用户要求 ZIP、教程或飞书交付时再调用 `skill-delivery-workflow`；未要求则不扩张交付物。

失败时保留备份和证据，禁止用“命令成功”代替真实验收。
