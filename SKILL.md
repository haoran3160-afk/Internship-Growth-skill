---
name: internship-growth-skill
description: Use whenever a requester identifies as a software intern or junior developer and wants learning or onboarding support for an unfamiliar codebase or business flow, especially company-internal code or uncertain output permission; also use for personal Obsidian design notes, evidence-backed internship worklogs, and truthful resume or interview material. Not for ordinary implementation, debugging, or review without a learning or internship-recording goal.
---

# Internship-Growth-skill

## 核心原则

一次只处理一个有边界的学习任务。识别用户当前需要的模式，只读取对应参考文件，只产出该模式的结果；不要自动扩展成知识管理、周报、Dashboard 或完整成长流程。

## 选择模式

| 当前意图 | 必读参考 | 可选模板 | 本次结果 |
|---|---|---|---|
| 理解仓库、功能、Bug、PR 或代码链路 | `references/understand.md` | `assets/feature-trace.md` | 有证据的链路解释与 Teach-back |
| 沉淀值得复用的设计 | `references/distill.md` | `assets/engineering-pattern.md` | 脱敏的工程模式笔记 |
| 记录工作或准备面试 | `references/experience.md` | `assets/worklog.md` 或 `assets/interview-story.md` | 归属和证据清晰的经历材料 |

当请求混合多个模式时，本次仍只选一个：用户明确给出顺序时，完成第一个尚未完成的前置模式；没有顺序时，选择当前输入有足够证据完成的最直接交付。把其余模式列为可选后续，不预生成其内容。理解与经历混合且身份尚未确认时，先交付理解结果，不写第一人称面试素材。

当内容来自非公开仓库、内部文档或团队工作时，在输出任何来源标识前读取 `references/privacy.md`，并把当前对话也视为一个待分类的目标位置。仅在用户要求保存文件时使用模板；否则按当前对话的隐私边界交付。

## 共同约束

- 先读取目标仓库自己的说明与最小相关文件。
- 目标位置获准保留内部证据时，用仓库相对 `path:line` 和 commit `source_ref` 支持关键技术结论；个人脱敏位置只用不可反查的证据句柄和核对日期，并明确不能独立复核。标记 `confirmed`、`inferred` 或 `unknown`。
- 围绕一个真实业务目标或问题追踪链路，不按目录逐一导览，不强行补齐仓库中不存在的层。
- 把公司私有内容留在获准位置；个人笔记只写脱敏事实、通用原理和独立重写的示例。
- 把 `owned`、`contributed`、`observed` 贴在最小可核验陈述上，不贴在整个任务上；Git 记录不能单独证明方案所有权或业务影响。
- 不把 `contributed` 当作归属未知时的保守默认值；三种标签都必须由事实支持。
- 先通过身份门禁再写第一人称经历：用户必须明确确认相关提交或行动属于自己，或提供“当前用户 ↔ 作者”的证据；“整理成我的经历”、本地 Git 配置、同一提交作者和本机目录都不算确认。
- 不虚构指标、因果、规模、上线状态或个人贡献。
- 使用用户的语言，先给结论，再给证据和未决问题。

## 停止条件

- **理解：** 当前链路已解释，关键结论有证据或不确定性标记，并给出一个需要学习者回答的 Teach-back 问题。不要同时给出答案；没有学习者回答时，不声称其已经理解。
- **沉淀：** 候选确有复用价值，默认结果只有一个模式、一个不变量、一个独立示例、一至三个验证、一个主要取舍和一个迁移题；个人版本不含可识别的内部实现。
- **经历：** 身份未确认时只交付不归属于任何人的待确认事实包；身份确认后，每个重要陈述都有归属和证据状态，无法证明的影响保持未知。

## 常见错误

| 错误 | 修正 |
|---|---|
| 一次生成所有产物 | 只完成当前模式。 |
| 用代理总结代替学习验证 | 让学习者复述、预测或定位故障。 |
| 把内部源码改名后放进个人库 | 关闭来源，按原理独立重写。 |
| 根据提交历史写“我负责” | 先确认作者、职责、决策者和验证证据。 |
| 归属未知时自动降级成 `contributed` | 仍保持未知，只输出待确认事实包。 |
| 给出 Teach-back 后立即自问自答 | 只提出一个问题并等待学习者作答。 |
