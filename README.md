# Internship Growth

[**简体中文**](./README.md) | [English](./README_EN.md)

> 帮程序员实习生看懂代码、沉淀工程知识、讲清真实经历。

**一个面向程序员实习生的 Codex Skill。**

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-5B5BD6)](./SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![No Runtime Dependencies](https://img.shields.io/badge/runtime_dependencies-0-success)](./SKILL.md)

`internship-growth` 覆盖程序员实习最关键的三个场景：进入陌生仓库时追踪业务与代码链路，遇到优秀设计时沉淀成可迁移的工程笔记，完成任务后把个人贡献整理成有证据的工作记录和面试素材。

每次调用围绕一个明确问题展开，并标注来源、归属和不确定性，方便后续复查、沉淀和面试准备。

## 它能做什么

| 模式 | 你提供什么 | Skill 做什么 | 你得到什么 |
|---|---|---|---|
| **理解** | 仓库路径 + 一个具体问题 | 追踪业务目标、代码节点、数据变化和失败路径，并标记证据状态 | 一条有证据的端到端链路 + 一个 Teach-back 问题 |
| **沉淀** | 已理解的设计 + 笔记目标位置 | 提炼不变量和取舍，脱离原仓库独立重写示例与验证 | 一篇可迁移、可验证、已脱敏的工程模式笔记 |
| **经历** | 工作事实 + 身份、职责和证据 | 拆分每条陈述，核对个人归属与证据状态 | 工作留痕，或基于已确认事实生成的 STAR-R 素材 |

**一次调用只完成一种模式。** 这样能缩小证据范围，减少未经验证的推断，并让停止条件保持清晰。

## 安装

### Windows PowerShell

```powershell
$internshipSkillRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME 'skills'
} else {
  Join-Path $env:USERPROFILE '.codex\skills'
}

New-Item -ItemType Directory -Force -Path $internshipSkillRoot | Out-Null
git clone https://github.com/haoran3160-afk/internship-skill.git `
  (Join-Path $internshipSkillRoot 'internship-growth')
```

### macOS / Linux

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/haoran3160-afk/internship-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/internship-growth"
```

安装完成后，新建一个 Codex 任务，让 Codex 重新发现 Skill 目录。首次使用建议显式写出 `$internship-growth`，避免与其他代码理解 Skill 发生路由竞争。

## 快速开始

先选择当前最需要解决的一件事，再使用对应模式。

### 1. 看懂一条代码链路

适合理解新仓库、新功能、Bug、PR 或陌生业务流程。

```text
使用 $internship-growth 的理解模式。

请在 <仓库路径> 中，围绕“订单提交后如何完成库存扣减”追踪端到端链路。
当前对话允许展示内部路径。
不要保存文件，最后只给一个 Teach-back 问题。
```

Skill 会围绕这个问题说明：

1. 业务目标和入口
2. 关键代码跳转
3. 数据如何变化
4. 失败路径和保护机制
5. 哪些结论已确认、来自推断或仍未知
6. 一个需要你亲自回答的 Teach-back 问题

它不会用目录导览代替链路，也不会替你完成最后的学习验证。

### 2. 沉淀一个工程设计

适合把已经看懂、且值得跨项目复用的设计整理进 Obsidian。请新建任务，并粘贴脱敏后的设计事实，或提供获准读取的理解结果。

```text
使用 $internship-growth 的沉淀模式。

以下是已确认的设计事实：<粘贴脱敏事实，或提供获准读取的文件路径>。
请把“库存扣减的幂等处理”整理成个人 Obsidian 草稿。
来源是非公开仓库；不要保留内部路径、命名、Commit 或源码。
```

默认笔记只保留六项：

1. 一个工程模式
2. 一个核心不变量
3. 一个独立重写的最小示例
4. 一至三个验证
5. 一个主要取舍
6. 一个迁移题

重点不是收藏一段公司代码，而是学会它解决了什么约束、为什么这样设计，以及何时不该使用。

### 3. 记录一段真实工作经历

适合日常工作留痕、简历准备和面试复盘。

```text
使用 $internship-growth 的经历模式。

我确认提交 abc123 和 def456 是我完成的。
Leader 决定整体方案；我负责接口实现和回归测试。
请生成工作留痕，不生成 STAR。
```

Skill 会把每项事实拆成最小可核验陈述，并分别记录：

- `claim_attribution`：`owned`、`contributed` 或 `observed`
- `evidence_status`：`verified`、`user-confirmed`、`inferred` 或 `unknown`
- `evidence_source`：用户确认、Git、PR、Issue、测试、运行结果或评审

如果身份或职责没有确认，它只返回待确认事实包，不生成第一人称简历或面试故事。Git 记录可以证明活动存在，但不能单独证明方案归属或业务影响。

## 推荐工作流

```text
选择一个具体问题
  → 理解：追踪链路并回答 Teach-back
  → 沉淀：把值得复用的设计独立重写成个人笔记
  → 经历：把真实工作整理成有归属、有证据的材料
```

三种模式可以前后衔接，但应放在不同任务中完成。不要一次要求仓库导览、知识库、周报、简历和 STAR；更小的任务边界会得到更准确的证据和更可靠的结果。

## 隐私与真实性

处理公司内部仓库、文档或团队工作前，先说明当前对话是否获准展示内部内容。

```text
当前对话未获准展示内部路径，请按个人脱敏边界解释。
```

在个人脱敏边界下，Skill 使用 `private-source`、`source_ref: withheld` 和 `E1`、`E2` 等不可反查句柄，不输出内部路径、Commit、接口标识或源码。

| 内容状态 | 含义 |
|---|---|
| `review-required` | 目标位置或授权尚未确认 |
| `company-internal` | 只能保存在公司批准的位置 |
| `personal-sanitized` | 已脱敏，可进入个人笔记，但不代表可以公开 |
| `public` | 来自公开来源或已获得明确公开许可 |

公司政策和明确授权始终优先于本 Skill。

## 内置模板

| 模板 | 用途 |
|---|---|
| [`feature-trace.md`](./assets/feature-trace.md) | 保存一条功能或问题的证据链路 |
| [`engineering-pattern.md`](./assets/engineering-pattern.md) | 保存一个脱敏的工程模式 |
| [`worklog.md`](./assets/worklog.md) | 记录逐条归属和证据 |
| [`interview-story.md`](./assets/interview-story.md) | 从已确认事实生成 STAR-R 素材 |

只有在你明确要求保存文件时才使用模板；默认直接在当前对话中交付结果。

## 为什么这样设计

- **学习必须经过验证。** 阅读 AI 总结不等于理解，Teach-back 用来暴露误解。
- **知识必须能够迁移。** 沉淀的是不变量、取舍和验证，不是可识别的内部实现。
- **经历必须能够核对。** 作者、职责、决策、部署和影响分别确认，不把团队成果写成个人所有。
- **隐私优先于证据展示。** 无法安全保留精确来源时，使用脱敏句柄并明确可复核边界。
- **功能保持轻量。** 项目没有运行时脚本、数据库、状态机或外部依赖。

## 项目结构

```text
internship-growth/
├── SKILL.md                    # 触发描述、模式路由和共同约束
├── agents/
│   └── openai.yaml            # Codex 展示与隐式调用元数据
├── references/
│   ├── understand.md          # 理解模式
│   ├── distill.md             # 沉淀模式
│   ├── experience.md          # 经历模式
│   └── privacy.md             # 隐私与输出位置边界
├── assets/
│   ├── feature-trace.md
│   ├── engineering-pattern.md
│   ├── worklog.md
│   └── interview-story.md
├── README.md                   # 中文主文档
├── README_EN.md                # English documentation
└── LICENSE
```

详细流程按模式从 `references/` 按需读取，避免加载无关上下文。

## 贡献

欢迎提交 Issue 或 Pull Request。每次变更建议只解决一个可观察问题，并说明：

1. 哪类真实请求触发了问题
2. 未修改 Skill 时出现了什么错误行为
3. 修改后如何验证触发、输出或安全边界

请避免加入 Dashboard、遥测、长期状态或与三种模式无关的工作流。

## License

[MIT](./LICENSE) © 2026 haoran3160-afk
