#!/usr/bin/env python3
"""Structural validation for this Skill repository.

Dev-time check only (used by CI); the Skill itself has no runtime dependency.
Uses the Python standard library exclusively.

Checks:
1. SKILL.md frontmatter has a valid `name` and a non-empty `description`.
2. Every file the Skill routes to (references/, assets/, agents/) exists.
3. Relative markdown links in all tracked .md files resolve to real files.
4. Asset templates keep `confidentiality: review-required` frontmatter and do
   not redefine the per-claim `evidence_status` enum at document level.
5. Attribution and evidence vocabularies are not accidentally dropped from the
   experience templates.
6. agents/openai.yaml keeps the keys Codex reads.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ROUTED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/understand.md",
    "references/distill.md",
    "references/experience.md",
    "references/privacy.md",
    "assets/feature-trace.md",
    "assets/engineering-pattern.md",
    "assets/worklog.md",
    "assets/interview-story.md",
]

TEMPLATE_FILES = [
    "assets/feature-trace.md",
    "assets/engineering-pattern.md",
    "assets/worklog.md",
    "assets/interview-story.md",
]

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024

MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

ATTRIBUTION_ENUM = ["owned", "contributed", "observed"]
EVIDENCE_STATUS_ENUM = ["verified", "user-confirmed", "inferred", "unknown"]

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_frontmatter(path: Path) -> dict[str, str]:
    """Parse the simple `key: value` frontmatter block of a markdown file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return frontmatter
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            frontmatter[match.group(1)] = match.group(2).strip().strip('"')
    return {}


def check_routed_files() -> None:
    for relative in ROUTED_FILES:
        if not (REPO_ROOT / relative).is_file():
            fail(f"missing routed file: {relative}")


def check_skill_frontmatter() -> None:
    skill_md = REPO_ROOT / "SKILL.md"
    if not skill_md.is_file():
        return
    frontmatter = read_frontmatter(skill_md)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        fail("SKILL.md frontmatter is missing `name`")
    elif not NAME_PATTERN.match(name):
        fail(f"SKILL.md `name` must be lowercase kebab-case, got: {name!r}")
    elif len(name) > MAX_NAME_LENGTH:
        fail(f"SKILL.md `name` exceeds {MAX_NAME_LENGTH} characters")

    if not description:
        fail("SKILL.md frontmatter is missing `description`")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        fail(f"SKILL.md `description` exceeds {MAX_DESCRIPTION_LENGTH} characters")


def check_markdown_links() -> None:
    for md_file in sorted(REPO_ROOT.rglob("*.md")):
        if ".git" in md_file.parts:
            continue
        text = md_file.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = target.split("#", 1)[0]
            if not relative_target:
                continue
            resolved = (md_file.parent / relative_target).resolve()
            if not resolved.exists():
                fail(
                    f"broken relative link in {md_file.relative_to(REPO_ROOT)}: {target}"
                )


def check_templates() -> None:
    for relative in TEMPLATE_FILES:
        template = REPO_ROOT / relative
        if not template.is_file():
            continue
        frontmatter = read_frontmatter(template)
        if frontmatter.get("confidentiality") != "review-required":
            fail(f"{relative}: frontmatter must default to `confidentiality: review-required`")
        if "evidence_status" in frontmatter:
            fail(
                f"{relative}: `evidence_status` is a per-claim enum defined in "
                "references/experience.md and must not be a document-level key"
            )

    for relative in ["assets/worklog.md", "assets/interview-story.md"]:
        template = REPO_ROOT / relative
        if not template.is_file():
            continue
        body = template.read_text(encoding="utf-8")
        for term in ATTRIBUTION_ENUM + EVIDENCE_STATUS_ENUM:
            if term not in body:
                fail(f"{relative}: vocabulary term `{term}` was dropped")


def check_openai_yaml() -> None:
    manifest = REPO_ROOT / "agents" / "openai.yaml"
    if not manifest.is_file():
        return
    text = manifest.read_text(encoding="utf-8")
    for key in ["display_name", "short_description", "default_prompt", "allow_implicit_invocation"]:
        if key not in text:
            fail(f"agents/openai.yaml is missing `{key}`")


def main() -> int:
    check_routed_files()
    check_skill_frontmatter()
    check_markdown_links()
    check_templates()
    check_openai_yaml()

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
