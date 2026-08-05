from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path

from scripts import validate_skill


REPO_ROOT = Path(__file__).resolve().parent.parent


class ValidatorBehaviorTests(unittest.TestCase):
    def make_repo_copy(self) -> Path:
        temp_root = REPO_ROOT / ".test-tmp" / uuid.uuid4().hex
        repo_root = temp_root / "skill"
        temp_root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, temp_root, True)
        shutil.copytree(
            REPO_ROOT,
            repo_root,
            ignore=shutil.ignore_patterns(".git", ".test-tmp", "__pycache__"),
        )
        return repo_root

    @staticmethod
    def replace_frontmatter(content: str, frontmatter: str) -> str:
        _, body = content.split("\n---\n", 1)
        return f"---\n{frontmatter}\n---\n{body}"

    def test_rejects_malformed_skill_frontmatter(self) -> None:
        repo_root = self.make_repo_copy()
        skill_md = repo_root / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        content = content.replace(
            "description: Use whenever",
            "description: [\n# Use whenever",
            1,
        )
        skill_md.write_text(content, encoding="utf-8")

        errors = validate_skill.validate(repo_root)

        self.assertTrue(
            any("SKILL.md" in error and "YAML" in error for error in errors),
            errors,
        )

    def test_accepts_current_repository(self) -> None:
        self.assertEqual(validate_skill.validate(REPO_ROOT), [])

    def test_accepts_crlf_yaml_files(self) -> None:
        repo_root = self.make_repo_copy()
        for relative in ["SKILL.md", "agents/openai.yaml"]:
            path = repo_root / relative
            content = path.read_text(encoding="utf-8")
            path.write_bytes(content.replace("\n", "\r\n").encode("utf-8"))

        self.assertEqual(validate_skill.validate(repo_root), [])

    def test_validation_does_not_leak_errors_between_runs(self) -> None:
        repo_root = self.make_repo_copy()
        skill_md = repo_root / "SKILL.md"
        valid_content = skill_md.read_text(encoding="utf-8")
        skill_md.write_text("invalid", encoding="utf-8")
        self.assertNotEqual(validate_skill.validate(repo_root), [])

        skill_md.write_text(valid_content, encoding="utf-8")

        self.assertEqual(validate_skill.validate(repo_root), [])

    def test_rejects_malformed_openai_yaml(self) -> None:
        repo_root = self.make_repo_copy()
        manifest = repo_root / "agents" / "openai.yaml"
        content = manifest.read_text(encoding="utf-8")
        manifest.write_text(content.replace("interface:", "interface: [", 1), encoding="utf-8")

        errors = validate_skill.validate(repo_root)

        self.assertTrue(
            any("agents/openai.yaml" in error and "YAML" in error for error in errors),
            errors,
        )

    def test_rejects_duplicate_yaml_keys(self) -> None:
        repo_root = self.make_repo_copy()
        skill_md = repo_root / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        skill_md.write_text(
            content.replace(
                "name: internship-growth-skill",
                "name: internship-growth-skill\nname: duplicate-name",
                1,
            ),
            encoding="utf-8",
        )

        errors = validate_skill.validate(repo_root)

        self.assertTrue(any("duplicate key" in error for error in errors), errors)

        repo_root = self.make_repo_copy()
        manifest = repo_root / "agents" / "openai.yaml"
        content = manifest.read_text(encoding="utf-8")
        manifest.write_text(
            content.replace(
                '  display_name: "Internship-Growth-skill"',
                '  display_name: "Internship-Growth-skill"\n  display_name: "duplicate"',
                1,
            ),
            encoding="utf-8",
        )

        errors = validate_skill.validate(repo_root)

        self.assertTrue(any("duplicate key" in error for error in errors), errors)

    def test_enforces_skill_frontmatter_schema(self) -> None:
        cases = [
            (
                "unknown key",
                lambda content: self.replace_frontmatter(
                    content,
                    "name: internship-growth-skill\n"
                    "description: valid description\n"
                    "extra: unexpected",
                ),
                "unknown frontmatter key",
            ),
            (
                "missing key",
                lambda content: self.replace_frontmatter(
                    content,
                    "name: internship-growth-skill",
                ),
                "missing frontmatter key",
            ),
            (
                "wrong type",
                lambda content: self.replace_frontmatter(
                    content,
                    "name: internship-growth-skill\ndescription: true",
                ),
                "`description` must be a non-empty string",
            ),
            (
                "non-mapping root",
                lambda content: self.replace_frontmatter(
                    content,
                    "- name\n- description",
                ),
                "must be a mapping",
            ),
            (
                "angle brackets",
                lambda content: self.replace_frontmatter(
                    content,
                    "name: internship-growth-skill\n"
                    "description: invalid <placeholder>",
                ),
                "angle brackets",
            ),
            (
                "missing closing delimiter",
                lambda content: content.replace("\n---\n", "\n", 1),
                "missing closing",
            ),
            (
                "UTF-8 BOM",
                lambda content: "\ufeff" + content,
                "BOM",
            ),
        ]

        for case_name, mutate, expected in cases:
            with self.subTest(case=case_name):
                repo_root = self.make_repo_copy()
                skill_md = repo_root / "SKILL.md"
                content = skill_md.read_text(encoding="utf-8")
                skill_md.write_text(mutate(content), encoding="utf-8")

                errors = validate_skill.validate(repo_root)

                self.assertTrue(any(expected in error for error in errors), errors)

    def test_enforces_openai_yaml_schema(self) -> None:
        cases = [
            (
                "unknown top-level key",
                lambda content: content + "\nextra: true\n",
                "unknown top-level key",
            ),
            (
                "missing top-level key",
                lambda content: content.split("policy:", 1)[0],
                "missing top-level key",
            ),
            (
                "unknown interface key",
                lambda content: content.replace(
                    "  display_name:",
                    "  unexpected: true\n  display_name:",
                    1,
                ),
                "unknown `interface` key",
            ),
            (
                "missing interface key",
                lambda content: "\n".join(
                    line
                    for line in content.splitlines()
                    if "short_description:" not in line
                ),
                "missing `interface` key",
            ),
            (
                "wrong interface value type",
                lambda content: content.replace(
                    'display_name: "Internship-Growth-skill"',
                    "display_name: true",
                    1,
                ),
                "`interface.display_name` must be a non-empty string",
            ),
            (
                "short description",
                lambda content: content.replace(
                    'short_description: "理解真实代码链路，沉淀工程模式，记录可验证实习经历"',
                    'short_description: "too short"',
                    1,
                ),
                "25–64 characters",
            ),
            (
                "default prompt missing skill token",
                lambda content: content.replace(
                    "$internship-growth-skill",
                    "Internship Growth",
                    1,
                ),
                "must contain `$internship-growth-skill`",
            ),
            (
                "unknown policy key",
                lambda content: content + "  unexpected: true\n",
                "unknown `policy` key",
            ),
            (
                "wrong boolean type",
                lambda content: content.replace(
                    "allow_implicit_invocation: true",
                    'allow_implicit_invocation: "true"',
                    1,
                ),
                "must be a boolean",
            ),
            (
                "non-mapping root",
                lambda content: "- interface\n- policy\n",
                "root must be a mapping",
            ),
            (
                "multiple YAML documents",
                lambda content: content + "\n---\n{}\n",
                "invalid YAML",
            ),
            (
                "UTF-8 BOM",
                lambda content: "\ufeff" + content,
                "BOM",
            ),
        ]

        for case_name, mutate, expected in cases:
            with self.subTest(case=case_name):
                repo_root = self.make_repo_copy()
                manifest = repo_root / "agents" / "openai.yaml"
                content = manifest.read_text(encoding="utf-8")
                manifest.write_text(mutate(content), encoding="utf-8")

                errors = validate_skill.validate(repo_root)

                self.assertTrue(any(expected in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
