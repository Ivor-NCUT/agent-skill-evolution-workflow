---
name: skill-evolution-validation-delivery
description: 验证、安装和同步 Agent Skill，并在用户明确要求时完成压缩包、教程或飞书交付。用于 Skill 创建或迭代完成后的 quick_validate、仓库测试、本地与云端版本一致性、兼容检查和系统提示更新。
---

# Skill 验证交付

一次交付只维护一张 `.skill-delivery-receipt.json` 收据，按下面四段顺序补齐；不要为
本地、GitHub、Zeabur 和登记表分别发明互不相认的状态。

## 1. 本地候选

1. 记录仓库、版本、基线 commit、用户原有未提交改动和本轮目标文件。
2. 运行每个变更 Skill 的 `quick_validate.py`、仓库 validator、测试和路由用例。
3. 校验来源、许可证、旧入口和公共路径；安装器只能管理自己的符号链接，真实目录
   先备份，不静默覆盖。
4. 在收据写入 `local.commit`、`local.version`、入口 Skill、`project.json` 与制品
   SHA-256，以及验证命令和结果。任一检查失败就停在本地，不发布。

## 2. GitHub 基线

1. GitHub 远端只使用 `gh` / `gh api`。先查重 Issue/PR，再创建可验收 Issue、唯一
   分支和 PR；不得把用户已有改动误当成本轮内容。
2. EOF 或超时后先回读 ref、PR、commit/tree SHA，只补缺失动作。
3. CI 通过并合并后，回读默认分支 commit/tree；确认本地候选与 GitHub 目标树一致，
   再写入 `github.commit`、`github.tree`、Issue/PR 和 CI 结果。

## 3. Zeabur 原子同步

1. 先用 Zeabur Skill 解析精确 project/service/environment，回读当前版本、安装路径、
   运行进程和健康；不要凭旧记忆覆盖。
2. 制品先完整归档并计算 SHA，再上传到新暂存目录。CLI 不转发本地 stdin 时使用
   Base64 分片并逐片回读累计字节；解包后用容器现有运行时验证 JSON、入口和 SHA。
3. 验证通过才执行“备份旧目录 -> 原子切换”。EOF 后回读目标版本、备份和 SHA，
   已切换则不重试。活跃任务默认不重启；只有运行时必须加载新版本且安全时才受控重启。
4. 回读入口 Skill、`project.json`、版本、三个 SHA 和生产健康，写入 `cloud` 与回滚路径。

## 4. 中央登记与收口

1. 只有本地、GitHub、云端实际版本确定后，才用现有 inventory 生成器更新
   `company-skills.json`；预览 diff，只接受目标部门版本、专家和安装状态变化。
2. 登记仓库按同一 GitHub 流程发布；云端只同步登记文件并保留备份。回读所有受影响
   条目的版本与安装状态，写入 `registry`。
3. 最终要求收据中的 `local/github/cloud/registry` 版本一致，入口与 `project.json` SHA
   一致，GitHub CI 和生产健康通过。无法部署云端时明确标为 `not_requested` 或
   `blocked`，不得用本地成功冒充四方完成。

收据只存提交、版本、SHA、链接、验证和回滚路径，不存 token、secret 或私有日志。
用户要求 ZIP、教程或飞书交付时再调用 `skill-delivery-workflow`；未要求则不扩张交付物。

失败时保留备份和证据，禁止用“命令成功”代替真实验收。
