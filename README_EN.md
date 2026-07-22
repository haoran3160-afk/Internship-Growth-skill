# Internship-Growth-skill

[简体中文](./README.md) | [**English**](./README_EN.md)

> Help software interns understand business and code, distill engineering knowledge, and articulate real experience.

**A Codex Skill for software interns.**

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-5B5BD6)](./SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![No Runtime Dependencies](https://img.shields.io/badge/runtime_dependencies-0-success)](./SKILL.md)

`internship-growth-skill` covers three critical situations in a software internship: tracing business and code flows in an unfamiliar repository, turning useful engineering designs into transferable notes, and organizing personal contributions into evidence-backed work records and interview material.

Each invocation focuses on one explicit question and marks sources, attribution, and uncertainty so that the result can be reviewed, distilled, or used for interview preparation later.

## What It Does

| Mode | What you provide | What the Skill does | What you receive |
|---|---|---|---|
| **Understand** | A repository path or code + one concrete question | Explains business, architecture, runtime mechanisms, critical code, and failure paths at the needed depth; marks evidence status | A readable explanation from mental map to critical implementation |
| **Distill** | An understood design + the target note location | Extracts invariants and trade-offs; independently rewrites examples and checks outside the source repository | A sanitized, verifiable, and transferable engineering pattern note |
| **Experience** | Work facts + identity, responsibilities, and evidence | Splits claims and checks attribution and evidence status for each one | A worklog or STAR-R material based only on confirmed facts |

**One invocation completes one mode only.** This keeps the evidence scope small, reduces unsupported inference, and gives each task a clear stopping condition.

## Installation

### Windows PowerShell

```powershell
$internshipSkillRoot = Join-Path $env:USERPROFILE '.agents\skills'

New-Item -ItemType Directory -Force -Path $internshipSkillRoot | Out-Null
git clone https://github.com/haoran3160-afk/Internship-Growth-skill.git `
  (Join-Path $internshipSkillRoot 'internship-growth-skill')
```

### macOS / Linux

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/haoran3160-afk/Internship-Growth-skill.git \
  "$HOME/.agents/skills/internship-growth-skill"
```

This is Codex's supported user-level Skill directory, so the Skill is available across repositories. To enable it for only one project, clone it to that project's `.agents/skills/internship-growth-skill` directory instead. If Codex does not detect it in the current task, restart Codex. For the first invocation, explicitly include `$internship-growth-skill` to avoid routing conflicts with other code-understanding Skills. See the [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) for discovery locations.

## Quick Start

Choose the single task you need most, then use the corresponding mode.

### 1. Understand a Code Flow

Use this mode to understand an unfamiliar repository, feature, bug, PR, or business flow.

```text
Use the understanding mode of $internship-growth-skill.

In <repository path>, trace the end-to-end flow for
“how inventory is deducted after an order is submitted.”
This conversation is authorized to display internal paths.
Do not save files. Use detailed depth by default so an intern
without repository context can follow the explanation.
```

The Skill explains:

1. Business context, actors, and critical rules
2. System boundaries, component responsibilities, and dependencies
3. How requests, data, state, or events move
4. What critical code does and why it exists
5. Data changes, failure paths, and verification evidence
6. Which conclusions are confirmed, inferred, or still unknown

The understanding mode selects depth from your intent: an explicit request for a quick orientation produces an overview; detailed explanation is the default; an explicit request for line-by-line, block-level, or function-level analysis starts a code deep dive. A code deep dive establishes business context and logical blocks before explaining critical lines instead of translating syntax in isolation.

Business understanding, architecture decomposition, runtime mechanisms, first principles analysis, and reverse tracing are composable analysis lenses. When a flow has at least three important nodes, meaningful branches, or cross-boundary interactions, the Skill can generate an evidence-backed logic diagram. It does not force a diagram for a simple flow. Teach-back appears only when you ask to check your understanding or start a learning exercise.

### 2. Distill an Engineering Design

Use this mode to move an understood, reusable design into Obsidian. Start a new task and paste sanitized design facts, or provide an approved location containing the understanding result.

```text
Use the distillation mode of $internship-growth-skill.

These design facts have been confirmed: <paste sanitized facts,
or provide an approved file path>.
Turn “idempotent inventory deduction” into a personal Obsidian draft.
The source is a non-public repository; do not retain internal paths,
names, commits, or source code.
```

By default, the note contains seven reader-first elements:

1. The problem the pattern solves
2. Applicable situations and boundaries
3. One core invariant
4. The mechanism that maintains the invariant
5. One independently rewritten minimal example
6. One to three checks
7. One primary trade-off

The goal is not to collect company code. It is to understand which constraint the design solves, why it works, and when it should not be used. A transfer question appears only when you explicitly request transfer practice or a mastery check.

### 3. Document Real Work Experience

Use this mode for daily worklogs, résumé preparation, and interview review.

```text
Use the experience mode of $internship-growth-skill.

I confirm that commits abc123 and def456 are my work.
The team lead chose the overall design; I implemented the API
and completed regression testing.
Generate a worklog, not a STAR story.
```

The Skill splits each fact into the smallest verifiable claim and records:

- `claim_attribution`: `owned`, `contributed`, or `observed`
- `evidence_status`: `verified`, `user-confirmed`, `inferred`, or `unknown`
- `evidence_source`: user confirmation, Git, PR, Issue, tests, runtime results, or review

If identity or responsibility is not confirmed, it returns a fact packet for confirmation instead of generating a first-person résumé bullet or interview story. Git history can prove that activity exists, but it cannot prove design ownership or business impact by itself.

## Recommended Workflow

```text
Choose one concrete question
  → Understand: move from a business and architecture map into runtime flow and critical code
  → Distill: independently rewrite reusable design knowledge as a personal note
  → Experience: turn real work into evidence-backed, correctly attributed material
```

The three modes can form a sequence, but they should be completed in separate tasks. Do not request a repository tour, knowledge base, weekly report, résumé, and STAR story in one prompt. Smaller task boundaries produce more precise evidence and more reliable results.

## Privacy and Truthfulness

Before working with an internal repository, document, or team activity, state whether the current conversation is authorized to display internal content.

```text
This conversation is not authorized to display internal paths.
Explain the result within a personal-sanitized boundary.
```

Within a personal-sanitized boundary, the Skill uses `private-source`, `source_ref: withheld`, and non-reversible handles such as `E1` and `E2`. It does not output internal paths, commits, interface identifiers, or source code.

| Content status | Meaning |
|---|---|
| `review-required` | The destination or authorization has not been confirmed |
| `company-internal` | The content may be stored only in a company-approved location |
| `personal-sanitized` | The content has been sanitized for personal notes, but is not necessarily public |
| `public` | The source is public or explicit permission to publish has been granted |

Company policy and explicit authorization always take precedence over this Skill.

## Built-in Templates

| Template | Purpose |
|---|---|
| [`feature-trace.md`](./assets/feature-trace.md) | Save a reader-first mental map, runtime flow, and evidence trail |
| [`engineering-pattern.md`](./assets/engineering-pattern.md) | Save a sanitized pattern with its problem, boundaries, mechanism, and checks |
| [`worklog.md`](./assets/worklog.md) | Record claim-level attribution and evidence |
| [`interview-story.md`](./assets/interview-story.md) | Build STAR-R material from confirmed facts |

Templates are used only when you explicitly request a saved file. By default, the result is delivered directly in the current conversation.

## Design Rationale

- **Understand first, verify on demand.** Detailed explanation builds the mental model; Teach-back is used only when the learner requests an understanding check.
- **Knowledge must transfer.** Distillation preserves invariants, trade-offs, and checks—not identifiable internal implementations.
- **Experience must be auditable.** Authorship, responsibility, decisions, deployment, and impact are confirmed separately so team outcomes are not claimed as individual ownership.
- **Privacy comes before visible evidence.** When precise sources cannot be retained safely, the Skill uses sanitized handles and states the review boundary.
- **The Skill stays lightweight.** The project has no runtime scripts, database, state machine, or external runtime dependency.

## Project Structure

```text
internship-growth-skill/
├── SKILL.md                    # Trigger description, mode routing, and shared constraints
├── agents/
│   └── openai.yaml            # Codex display and implicit invocation metadata
├── references/
│   ├── understand.md          # Understanding mode
│   ├── distill.md             # Distillation mode
│   ├── experience.md          # Experience mode
│   └── privacy.md             # Privacy and destination boundaries
├── assets/
│   ├── feature-trace.md
│   ├── engineering-pattern.md
│   ├── worklog.md
│   └── interview-story.md
├── evals/
│   └── understanding-experience.md # Understanding-experience regression cases
├── docs/superpowers/             # Approved specification and implementation plan
├── README.md                   # Chinese documentation (default)
├── README_EN.md                # English documentation
└── LICENSE
```

Detailed instructions are loaded from `references/` only for the selected mode, avoiding irrelevant context.

## Contributing

Issues and pull requests are welcome. Each change should address one observable problem and explain:

1. Which real request exposed the problem
2. What incorrect behavior occurred before the change
3. How the updated trigger, output, or safety boundary was verified

Please avoid adding dashboards, telemetry, long-lived state, or workflows unrelated to the three modes.

## License

[MIT](./LICENSE) © 2026 haoran3160-afk
