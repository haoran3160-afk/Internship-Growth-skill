# Internship Growth

> 为程序员实习生设计的轻量 Codex Skill：理解真实代码仓库，沉淀可迁移的工程知识，把实际工作整理成可信经历。

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-5B5BD6)](./SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![No Runtime Dependencies](https://img.shields.io/badge/runtime_dependencies-0-success)](./SKILL.md)

`internship-growth` 只解决一次具体的实习学习任务。它不是 Dashboard、周报系统或知识库平台，也不会替你宣称已经理解代码、拥有团队成果或取得未经证实的业务指标。

## 为什么使用它

| 模式 | 你遇到的问题 | Skill 的结果 |
|---|---|---|
| **理解** | 新仓库、新功能、Bug 或 PR 看不懂 | 有证据的端到端链路解释 + 一个 Teach-back 问题 |
| **沉淀** | 看到好设计，却只会复制公司代码 | 脱敏、独立重写、可迁移的工程模式笔记 |
| **经历** | 做过工作，但无法准确写进简历或面试 | 逐条归属、逐条证据的工作记录或 STAR 素材 |

核心约束：**一次调用只完成一个模式。**

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

安装后创建一个新的 Codex 任务，使 Skill 目录重新被发现。

## 5 分钟上手

显式调用最稳定：在请求中写出 `$internship-growth`。Skill 也允许隐式触发，但当环境中存在其他代码理解 Skill 时，显式调用能避免路由竞争。

### 1. 理解一条真实链路

```text
使用 $internship-growth 的理解模式。

请在 <仓库路径> 中围绕“订单提交后如何完成库存扣减”追踪端到端链路。
当前对话允许展示内部路径。
不要保存文件，最后只给一个 Teach-back 问题。
```

输出会包含当前问题的业务目标、代码跳转、数据变化、失败路径、证据状态和一个需要你亲自回答的问题。Skill 不会替你回答 Teach-back 后再宣称你已经掌握。

### 2. 沉淀一个工程模式

先完成理解，再开启一个新任务：

```text
使用 $internship-growth 的沉淀模式。

把刚才学到的“库存扣减幂等设计”整理成个人 Obsidian 草稿。
仓库按非公开处理，只沉淀一个工程模式。
```

默认笔记只有六个组成：

1. 一个工程模式
2. 一个核心不变量
3. 一个独立重写的最小示例
4. 一至三个验证
5. 一个主要取舍
6. 一个迁移题

### 3. 记录真实经历

```text
使用 $internship-growth 的经历模式。

我确认提交 abc123 和 def456 是我完成的。
Leader 决定整体方案；我负责接口实现和回归测试。
请生成工作留痕，不生成 STAR。
```

每条陈述都会分别记录：

- `claim_attribution`：`owned`、`contributed` 或 `observed`
- `evidence_status`：`verified`、`user-confirmed`、`inferred` 或 `unknown`
- `evidence_source`：用户确认、Git、PR、Issue、测试、运行结果或评审

如果身份或职责尚未确认，Skill 只返回待确认事实包，不生成第一人称简历或面试故事。

## 推荐工作流

```text
选择一个具体问题
  → 理解模式
  → 回答 Teach-back
  → 值得跨项目复用时，新开任务进入沉淀模式
  → 形成真实工作证据后，新开任务进入经历模式
```

不要在一次请求中同时要求仓库导览、知识库、周报、简历和 STAR。更小的任务边界会得到更准确的证据、更短的输出和更可靠的学习反馈。

## 隐私与真实性

处理公司内部仓库前，请说明当前对话是否获准展示内部内容。

```text
当前对话未获准展示内部路径，请按个人脱敏边界解释。
```

此时 Skill 会使用 `private-source`、`source_ref: withheld` 和 `E1`、`E2` 等不可反查句柄，不输出内部路径、Commit、接口标识或源码。

四种内容状态：

| 状态 | 含义 |
|---|---|
| `review-required` | 目标位置或授权尚未确认 |
| `company-internal` | 只保存在公司批准的位置 |
| `personal-sanitized` | 已脱敏，可进入个人笔记，但不等于可公开 |
| `public` | 来自公开来源或已获明确公开许可 |

公司政策与明确授权始终优先于本 Skill。

## 内置模板

| 模板 | 用途 |
|---|---|
| [`feature-trace.md`](./assets/feature-trace.md) | 保存一条功能或问题的证据链路 |
| [`engineering-pattern.md`](./assets/engineering-pattern.md) | 保存一个脱敏工程模式 |
| [`worklog.md`](./assets/worklog.md) | 记录逐条归属和证据 |
| [`interview-story.md`](./assets/interview-story.md) | 从已确认事实生成 STAR-R 素材 |

模板只在你明确要求保存文件时使用；默认直接在对话中交付结果。

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
├── README.md
└── LICENSE
```

项目没有运行时脚本、数据库、状态机或外部依赖。详细流程按模式从 `references/` 按需加载，避免无关上下文占用。

## 设计原则

- **学习不是阅读完成。** 必须通过 Teach-back 暴露误解。
- **沉淀不是复制源码。** 个人示例必须脱离来源独立重写。
- **Git 不是所有权证明。** 作者、职责、决策、部署和影响分别核对。
- **隐私优先于可复核性。** 个人内容无法安全保留精确证据时，明确标记不可独立复核。
- **默认保持轻量。** 没有重复且确定性的需求，不增加脚本或管理系统。

## 贡献

欢迎提交 Issue 或 Pull Request。建议每次变更只解决一个可观察问题，并说明：

1. 哪类真实请求触发了问题
2. 未修改 Skill 时产生了什么错误行为
3. 修改后如何验证触发、输出或安全边界

请避免加入 Dashboard、遥测、长期状态或与三种模式无关的工作流。

## License

[MIT](./LICENSE) © 2026 haoran3160-afk
