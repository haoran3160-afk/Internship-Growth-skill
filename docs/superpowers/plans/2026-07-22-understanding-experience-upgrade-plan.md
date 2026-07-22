# Internship Growth 理解体验最小升级实施计划

## 状态

- 依据规格：`docs/superpowers/specs/2026-07-22-understanding-experience-upgrade-design.md`
- 当前阶段：等待用户确认计划。
- 实施原则：先记录失败案例，再做最小行为修改，最后同步文档和验证。

## 目标

在不增加模式、脚本、依赖或长期状态的前提下，让理解模式默认提供适合实习生的详细解释，并将 Teach-back 与迁移题从强制交付改为按需学习检验。

## 边界

### 始终执行

- 保持“一次一个任务、一次一个模式”。
- 保持证据、隐私、真实性和归属门禁。
- 使用 `apply_patch` 修改文件。
- 每完成一项任务立即执行对应验证。
- 提交前运行官方 Skill validator 和 `git diff --check`。

### 本次不执行

- 不增加任务规划第四模式。
- 不增加通用会议总结。
- 不修改 `references/privacy.md`、`references/experience.md`、经历模板或数据模型。
- 不修改 `agents/openai.yaml`。
- 不新增脚本、依赖、Dashboard、周报或持久状态。
- 不修改或提交用户未跟踪的 `.skillhub.json`。
- 不推送远程仓库，除非用户另行要求。

## 工具与命令

工作目录：

```powershell
Set-Location -LiteralPath 'D:\personal\internship-growth'
```

官方 Skill 校验：

```powershell
python 'C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'D:\personal\internship-growth'
```

差异与工作树校验：

```powershell
git diff --check
git diff --name-only
git status --short
```

## 依赖顺序

```text
任务 1：建立失败基线
  ├─→ 任务 2：理解模式行为
  ├─→ 任务 3：沉淀模式行为
  └─→ 任务 4：理解模板
          ↓
任务 5：同步中英文 README
          ↓
任务 6：回归验证与提交
```

任务 2、3、4 在逻辑上可以独立设计，但在同一工作树中按顺序实施和验证，避免未完成状态相互掩盖。

## 任务 1：建立失败基线和回归案例

修改文件：

- 新建 `evals/understanding-experience.md`

实施内容：

1. 记录用户已经观察到的三个真实失败：解释不够详细、强制 Teach-back 或迁移题、模板不直观。
2. 写入规格中的八个场景：详细解释、概览、代码下钻、逻辑图、第一性原理、逆向拆解、无强制学习检验、拒绝扩大范围。
3. 为每个场景记录输入、预期行为、修改前状态和证据位置。
4. 将修改前状态标为失败或已有保护；不得伪造实际模型运行结果。

验收：

- 三个用户反馈都能映射到至少一个失败场景。
- 每个场景有可观察的通过条件。
- 基线明确区分“用户实测”“静态指令检查”和“尚未运行”。

验证：

```powershell
rg -n "详细解释|概览|代码下钻|逻辑图|第一性原理|逆向拆解|学习检验|扩大范围" 'evals\understanding-experience.md'
rg -n "用户实测|静态检查|尚未运行" 'evals\understanding-experience.md'
```

## 任务 2：重构理解模式行为

修改文件：

- `SKILL.md`
- `references/understand.md`

实施内容：

1. 保持三种模式路由不变，将理解模式结果改为“按所需深度解释业务、架构、运行链路和代码”。
2. 将默认理解深度设为“详细”；只有用户明确要求快速全貌时使用概览，明确要求逐行或深入某段代码时使用代码下钻。
3. 在理解参考中定义业务、架构、运行机制、第一性原理和逆向追踪视角的可观察触发条件，并定义逻辑图的使用条件。
4. 使用“先地图、后下钻”的正向输出契约，要求关键解释回答做什么、为什么、输入输出、状态或副作用、下一跳和证据。
5. 保留来源快照、`path:line`、`source_ref`、隐私位置和置信度规则。
6. 将 Teach-back 改为仅在用户明确要求学习检验或主动复述时使用。
7. 调整停止条件和常见错误，不再要求默认提问。

验收：

- `SKILL.md` 仍只有理解、沉淀、经历三种模式。
- `references/understand.md` 明确定义三档深度、五种按需分析视角和逻辑图表达条件。
- 详细解释是实习生请求的默认值。
- 不存在强制 Teach-back 的完成条件。
- 证据和隐私规则没有被删除或放宽。

验证：

```powershell
rg -n "概览|详细|代码下钻" 'references\understand.md'
rg -n "业务理解|架构拆解|运行机制|第一性原理|逆向|逻辑图" 'references\understand.md'
rg -n "source_ref|path:line|confirmed|inferred|unknown" 'references\understand.md'
rg -n "明确要求.*学习检验|主动复述" 'references\understand.md'
```

## 任务 3：移除沉淀模式的强制迁移题

修改文件：

- `references/distill.md`
- `assets/engineering-pattern.md`

实施内容：

1. 将默认模式笔记改为问题、适用边界、不变量、机制、独立示例、验证和主要取舍。
2. 将迁移题改为可选学习检验，不再是默认输出和完成条件。
3. 保持复用价值门槛、独立重写、脱敏和失败导向验证要求。
4. 删除模板中强制 `pending` 学习状态，保留 `confidentiality`。

验收：

- 用户只要求生成 Obsidian 模式笔记时不会收到迁移题。
- 用户要求检查迁移能力时仍有明确执行方法。
- 独立重写与隐私要求完整保留。
- 模板正文按阅读顺序组织，不以数量口号作为标题。

验证：

```powershell
rg -n "问题|适用边界|核心不变量|工作机制|独立重写|验证|主要取舍" 'references\distill.md' 'assets\engineering-pattern.md'
rg -n "明确要求.*迁移|学习检验" 'references\distill.md' 'assets\engineering-pattern.md'
rg -n "confidentiality" 'assets\engineering-pattern.md'
```

## 任务 4：将理解模板改为阅读优先

修改文件：

- `assets/feature-trace.md`

实施内容：

1. 保留来源、版本、核对日期和隐私 frontmatter。
2. 正文依次呈现快速结论、业务背景、心智地图、运行链路、组件职责、关键实现、数据状态、失败验证和未决问题。
3. 将证据放在支持的结论旁，减少正文开头的宽表。
4. 将学习检验设为可选章节。
5. 保留个人脱敏位置对证据句柄和不可复核性的说明。

验收：

- 阅读者无需先理解证据 schema 就能获得业务和系统全貌。
- 核心结论仍能回到来源或句柄。
- 模板没有强制 Teach-back 状态。
- 模板没有引入新隐私字段或授权含义。

验证：

```powershell
rg -n "快速结论|业务背景|心智地图|运行链路|组件职责|关键实现|数据与状态|失败与验证|未决问题" 'assets\feature-trace.md'
rg -n "source_ref|verified_at|confidentiality|不可反查" 'assets\feature-trace.md'
```

## 任务 5：同步中英文用户文档

修改文件：

- `README.md`
- `README_EN.md`

实施内容：

1. 将理解模式描述改为默认详细解释，并说明概览和代码下钻选项。
2. 介绍业务理解、架构拆解、运行机制、第一性原理和逆向追踪是按需视角，逻辑图是按需表达形式；它们都不是新模式。
3. 删除“每次必须 Teach-back”或“每篇必须迁移题”的产品承诺。
4. 更新模板说明和示例输出，使中英文行为一致。
5. 保留三种模式、隐私、真实性和轻量边界说明。

验收：

- 中英文 README 都准确反映实现后的行为。
- README 不宣称存在任务规划或通用会议总结。
- 安装命令、仓库地址和现有隐私说明不受影响。

验证：

```powershell
rg -n "概览|详细|代码下钻|架构|第一性原理|逆向" 'README.md'
rg -n "overview|detailed|code deep dive|architecture|first principles|reverse" 'README_EN.md'
rg -n "三种模式|three modes" 'README.md' 'README_EN.md'
```

## 任务 6：回归验证、复审和提交

修改文件：

- 更新 `evals/understanding-experience.md` 的实施后静态检查结果。

实施内容：

1. 按八个场景逐项检查新的行为契约。
2. 将静态检查能够证明的项目标为通过；需要真实仓库输入或独立模型运行的项目明确保留为待前向测试。
3. 运行官方 Skill validator。
4. 检查空白错误、范围外文件和中英文一致性。
5. 确认 `.skillhub.json` 与 `agents/openai.yaml` 未进入差异。
6. 只暂存本计划列出的实现文件并创建一个实现提交；不推送。

完整验证：

```powershell
python 'C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'D:\personal\internship-growth'
git diff --check
git diff --name-only
git status --short
```

预期变更集合：

```text
SKILL.md
README.md
README_EN.md
assets/engineering-pattern.md
assets/feature-trace.md
evals/understanding-experience.md
references/distill.md
references/understand.md
```

验收：

- 官方 validator 输出 `Skill is valid!`。
- `git diff --check` 无输出。
- 差异只包含预期变更集合。
- `.skillhub.json` 仍为未跟踪且未暂存。
- `agents/openai.yaml` 无差异。
- 实现提交不包含计划或规格之外的行为扩展。

## 风险与检查点

| 检查点 | 主要风险 | 通过条件 |
|---|---|---|
| 基线完成 | 把设计判断伪装成真实模型结果 | 明确标注证据类型 |
| 理解规则完成 | 输出过长或删除证据门禁 | 三档深度存在，证据规则保留 |
| 沉淀规则完成 | 取消问题后也取消学习能力 | 学习检验仍可按需触发 |
| 模板完成 | 阅读友好但无法复核 | 结论旁保留来源或句柄 |
| README 完成 | 宣传超出实际行为 | 中英文只描述已实现能力 |
| 最终验证 | 混入用户文件或范围外改动 | 变更集合精确匹配 |

## 完成定义

只有同时满足以下条件才算实施完成：

- 八个回归场景均有明确结果。
- 真实用户反馈对应的三个失败都被直接修复。
- 三种模式、隐私和证据主线未改变。
- Skill 校验、差异检查和范围检查全部通过。
- 实现已提交但未推送，用户文件未被纳入提交。
