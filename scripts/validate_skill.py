#!/usr/bin/env python3
"""Structural validation for this Skill repository.

Dev-time check only (used by CI); the Skill itself has no runtime dependency.

Checks:
1. SKILL.md frontmatter has a valid `name` and a non-empty `description`.
2. Every file the Skill routes to (references/, assets/, agents/) exists.
3. Relative markdown links in Markdown files in the checkout resolve to real files.
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

import yaml
from yaml.constructor import ConstructorError
from yaml.resolver import BaseResolver

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


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that reports duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeySafeLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_frontmatter(path: Path, errors: list[str]) -> dict[object, object] | None:
    """Parse a Markdown file's opening YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        fail(errors, f"{path.name}: UTF-8 BOM is not allowed")
        return None
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(errors, f"{path.name}: missing opening YAML frontmatter delimiter")
        return None
    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        fail(errors, f"{path.name}: missing closing YAML frontmatter delimiter")
        return None
    yaml_text = "\n".join(lines[1:closing_index])
    try:
        frontmatter = yaml.load(yaml_text, Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        fail(errors, f"{path.name}: invalid YAML frontmatter: {exc}")
        return None
    if not isinstance(frontmatter, dict):
        fail(errors, f"{path.name}: YAML frontmatter must be a mapping")
        return None
    return frontmatter


def check_routed_files(repo_root: Path, errors: list[str]) -> None:
    for relative in ROUTED_FILES:
        if not (repo_root / relative).is_file():
            fail(errors, f"missing routed file: {relative}")


def check_skill_frontmatter(repo_root: Path, errors: list[str]) -> None:
    skill_md = repo_root / "SKILL.md"
    if not skill_md.is_file():
        return
    frontmatter = read_frontmatter(skill_md, errors)
    if frontmatter is None:
        return

    expected_keys = {"name", "description"}
    actual_keys = set(frontmatter)
    missing_keys = sorted(expected_keys - actual_keys)
    unknown_keys = sorted(actual_keys - expected_keys, key=repr)
    if missing_keys:
        fail(
            errors,
            "SKILL.md: missing frontmatter key(s): "
            + ", ".join(f"`{key}`" for key in missing_keys),
        )
    if unknown_keys:
        fail(
            errors,
            "SKILL.md: unknown frontmatter key(s): "
            + ", ".join(repr(key) for key in unknown_keys),
        )

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if "name" in frontmatter:
        if not isinstance(name, str) or not name.strip():
            fail(errors, "SKILL.md: `name` must be a non-empty string")
        elif not NAME_PATTERN.match(name):
            fail(errors, f"SKILL.md `name` must be lowercase kebab-case, got: {name!r}")
        elif len(name) > MAX_NAME_LENGTH:
            fail(errors, f"SKILL.md `name` exceeds {MAX_NAME_LENGTH} characters")

    if "description" in frontmatter:
        if not isinstance(description, str) or not description.strip():
            fail(errors, "SKILL.md: `description` must be a non-empty string")
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            fail(errors, f"SKILL.md `description` exceeds {MAX_DESCRIPTION_LENGTH} characters")
        elif "<" in description or ">" in description:
            fail(errors, "SKILL.md: `description` cannot contain angle brackets")


def check_markdown_links(repo_root: Path, errors: list[str]) -> None:
    for md_file in sorted(repo_root.rglob("*.md")):
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
                    errors,
                    f"broken relative link in {md_file.relative_to(repo_root)}: {target}",
                )


def check_templates(repo_root: Path, errors: list[str]) -> None:
    for relative in TEMPLATE_FILES:
        template = repo_root / relative
        if not template.is_file():
            continue
        frontmatter = read_frontmatter(template, errors)
        if frontmatter is None:
            continue
        if frontmatter.get("confidentiality") != "review-required":
            fail(errors, f"{relative}: frontmatter must default to `confidentiality: review-required`")
        if "evidence_status" in frontmatter:
            fail(
                errors,
                f"{relative}: `evidence_status` is a per-claim enum defined in "
                "references/experience.md and must not be a document-level key",
            )

    for relative in ["assets/worklog.md", "assets/interview-story.md"]:
        template = repo_root / relative
        if not template.is_file():
            continue
        body = template.read_text(encoding="utf-8")
        for term in ATTRIBUTION_ENUM + EVIDENCE_STATUS_ENUM:
            if term not in body:
                fail(errors, f"{relative}: vocabulary term `{term}` was dropped")


def check_openai_yaml(repo_root: Path, errors: list[str]) -> None:
    manifest = repo_root / "agents" / "openai.yaml"
    if not manifest.is_file():
        return
    text = manifest.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        fail(errors, "agents/openai.yaml: UTF-8 BOM is not allowed")
        return
    try:
        data = yaml.load(text, Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        fail(errors, f"agents/openai.yaml: invalid YAML: {exc}")
        return
    if not isinstance(data, dict):
        fail(errors, "agents/openai.yaml: document root must be a mapping")
        return

    expected_top_keys = {"interface", "policy"}
    actual_top_keys = set(data)
    missing_top_keys = sorted(expected_top_keys - actual_top_keys)
    unknown_top_keys = sorted(actual_top_keys - expected_top_keys, key=repr)
    if missing_top_keys:
        fail(
            errors,
            "agents/openai.yaml: missing top-level key(s): "
            + ", ".join(f"`{key}`" for key in missing_top_keys),
        )
    if unknown_top_keys:
        fail(
            errors,
            "agents/openai.yaml: unknown top-level key(s): "
            + ", ".join(repr(key) for key in unknown_top_keys),
        )

    interface = data.get("interface")
    policy = data.get("policy")
    if "interface" in data and not isinstance(interface, dict):
        fail(errors, "agents/openai.yaml: `interface` must be a mapping")
    elif isinstance(interface, dict):
        expected_interface_keys = {
            "display_name",
            "short_description",
            "default_prompt",
        }
        actual_interface_keys = set(interface)
        missing_interface_keys = sorted(expected_interface_keys - actual_interface_keys)
        unknown_interface_keys = sorted(
            actual_interface_keys - expected_interface_keys,
            key=repr,
        )
        if missing_interface_keys:
            fail(
                errors,
                "agents/openai.yaml: missing `interface` key(s): "
                + ", ".join(f"`{key}`" for key in missing_interface_keys),
            )
        if unknown_interface_keys:
            fail(
                errors,
                "agents/openai.yaml: unknown `interface` key(s): "
                + ", ".join(repr(key) for key in unknown_interface_keys),
            )

        for key in expected_interface_keys:
            if key not in interface:
                continue
            value = interface[key]
            if not isinstance(value, str) or not value.strip():
                fail(
                    errors,
                    f"agents/openai.yaml: `interface.{key}` must be a non-empty string",
                )

        short_description = interface.get("short_description")
        if isinstance(short_description, str) and short_description.strip():
            if not 25 <= len(short_description) <= 64:
                fail(
                    errors,
                    "agents/openai.yaml: `interface.short_description` must be 25–64 characters",
                )

        default_prompt = interface.get("default_prompt")
        if isinstance(default_prompt, str) and default_prompt.strip():
            if "$internship-growth-skill" not in default_prompt:
                fail(
                    errors,
                    "agents/openai.yaml: `interface.default_prompt` must contain "
                    "`$internship-growth-skill`",
                )

    if "policy" in data and not isinstance(policy, dict):
        fail(errors, "agents/openai.yaml: `policy` must be a mapping")
    elif isinstance(policy, dict):
        expected_policy_keys = {"allow_implicit_invocation"}
        actual_policy_keys = set(policy)
        missing_policy_keys = sorted(expected_policy_keys - actual_policy_keys)
        unknown_policy_keys = sorted(actual_policy_keys - expected_policy_keys, key=repr)
        if missing_policy_keys:
            fail(
                errors,
                "agents/openai.yaml: missing `policy` key(s): "
                + ", ".join(f"`{key}`" for key in missing_policy_keys),
            )
        if unknown_policy_keys:
            fail(
                errors,
                "agents/openai.yaml: unknown `policy` key(s): "
                + ", ".join(repr(key) for key in unknown_policy_keys),
            )

        allow_implicit = policy.get("allow_implicit_invocation")
        if "allow_implicit_invocation" in policy and type(allow_implicit) is not bool:
            fail(
                errors,
                "agents/openai.yaml: `policy.allow_implicit_invocation` must be a boolean",
            )


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []
    check_routed_files(repo_root, errors)
    check_skill_frontmatter(repo_root, errors)
    check_markdown_links(repo_root, errors)
    check_templates(repo_root, errors)
    check_openai_yaml(repo_root, errors)
    return errors


def main() -> int:
    errors = validate(REPO_ROOT)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
