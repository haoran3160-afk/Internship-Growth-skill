# Internship-Growth-skill

[简体中文](./README.md) | [**English**](./README_EN.md)

> Help software interns understand code, distill engineering knowledge, and articulate real experience.

**A Codex Skill for software interns.**

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-5B5BD6)](./SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![No Runtime Dependencies](https://img.shields.io/badge/runtime_dependencies-0-success)](./SKILL.md)

`internship-growth-skill` covers three critical situations in a software internship: tracing business and code flows in an unfamiliar repository, turning useful engineering designs into transferable notes, and organizing personal contributions into evidence-backed work records and interview material.

Each invocation focuses on one explicit question and marks sources, attribution, and uncertainty so that the result can be reviewed, distilled, or used for interview preparation later.

## What It Does

| Mode | What you provide | What the Skill does | What you receive |
|---|---|---|---|
| **Understand** | A repository path + one concrete question | Traces the business goal, code nodes, data changes, and failure paths; marks evidence status | An evidence-backed end-to-end trace + one Teach-back question |
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
Do not save files. End with one Teach-back question only.
```

The Skill explains:

1. The business goal and entry point
2. Critical code transitions
3. How data changes
4. Failure paths and safeguards
5. Which conclusions are confirmed, inferred, or still unknown
6. One Teach-back question that you must answer yourself

It does not replace a flow trace with a directory tour, and it does not complete the final learning check for you.

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

By default, the note contains only six elements:

1. One engineering pattern
2. One core invariant
3. One independently rewritten minimal example
4. One to three checks
5. One primary trade-off
6. One transfer question

The goal is not to collect company code. It is to understand which constraint the design solves, why it works, and when it should not be used.

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
  → Understand: trace the flow and answer the Teach-back
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
| [`feature-trace.md`](./assets/feature-trace.md) | Save the evidence trail for one feature or problem |
| [`engineering-pattern.md`](./assets/engineering-pattern.md) | Save one sanitized engineering pattern |
| [`worklog.md`](./assets/worklog.md) | Record claim-level attribution and evidence |
| [`interview-story.md`](./assets/interview-story.md) | Build STAR-R material from confirmed facts |

Templates are used only when you explicitly request a saved file. By default, the result is delivered directly in the current conversation.

## Design Rationale

- **Learning must be verified.** Reading an AI summary is not understanding; Teach-back exposes misconceptions.
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
