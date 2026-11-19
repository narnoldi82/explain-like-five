"""Content-integrity tests for the explain-like-five skill repository.

Runs with the standard library only:
    python -m pytest tests/test_skill.py
    python -m unittest discover tests
"""
import json
import re
import unittest
from pathlib import Path

# Resolve the repository root relative to this test file.
REPO_ROOT = Path(__file__).parent.parent
PLUGIN_JSON = REPO_ROOT / "plugin.json"
SKILL_MD = REPO_ROOT / "skills" / "explain-like-five" / "SKILL.md"
README_MD = REPO_ROOT / "README.md"
LICENSE_FILE = REPO_ROOT / "LICENSE"


class TestPluginJson(unittest.TestCase):
    """Tests for plugin.json structure and values."""

    def setUp(self):
        self.raw = PLUGIN_JSON.read_text(encoding="utf-8")
        self.data = json.loads(self.raw)

    def test_plugin_json_is_valid_json(self):
        """plugin.json must parse as valid JSON."""
        # If setUp succeeded, parsing already worked.
        self.assertIsInstance(self.data, dict)

    def test_plugin_json_required_fields(self):
        """plugin.json must contain name, version, description, license, author."""
        for field in ("name", "version", "description", "license", "author"):
            with self.subTest(field=field):
                self.assertIn(field, self.data, f"Missing required field: {field}")

    def test_plugin_json_name(self):
        """plugin.json name must be 'explain-like-five'."""
        self.assertEqual(self.data.get("name"), "explain-like-five")

    def test_plugin_json_license(self):
        """plugin.json license must be 'MIT'."""
        self.assertEqual(self.data.get("license"), "MIT")

    def test_plugin_json_version_format(self):
        """plugin.json version must follow MAJOR.MINOR.PATCH semver."""
        version = self.data.get("version", "")
        self.assertRegex(
            version,
            r"^\d+\.\d+\.\d+",
            f"version '{version}' does not match MAJOR.MINOR.PATCH",
        )


class TestSkillMd(unittest.TestCase):
    """Tests for skills/explain-like-five/SKILL.md structure and content."""

    def setUp(self):
        self.content = SKILL_MD.read_text(encoding="utf-8")
        # Parse YAML-style front-matter between the first pair of '---' lines.
        fm_match = re.match(r"^---\n(.*?)\n---", self.content, re.DOTALL)
        self.frontmatter = fm_match.group(1) if fm_match else ""

    def test_skill_md_exists(self):
        """SKILL.md must exist and be readable."""
        self.assertTrue(SKILL_MD.is_file(), f"SKILL.md not found at {SKILL_MD}")
        self.assertGreater(len(self.content), 0, "SKILL.md is empty")

    def test_skill_md_frontmatter_fields(self):
        """SKILL.md front-matter must contain name, version, license, description."""
        for field in ("name", "version", "license", "description"):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.frontmatter,
                    f"Front-matter missing field: {field}",
                )

    def test_skill_md_name_matches_plugin(self):
        """SKILL.md front-matter name must match plugin.json name."""
        plugin_data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
        plugin_name = plugin_data.get("name", "")
        # Extract the name value from front-matter (e.g. 'name: explain-like-five')
        fm_name_match = re.search(r"^name:\s*(.+)$", self.frontmatter, re.MULTILINE)
        self.assertIsNotNone(fm_name_match, "Could not find 'name' in SKILL.md front-matter")
        skill_name = fm_name_match.group(1).strip().strip("'\"")
        self.assertEqual(
            skill_name,
            plugin_name,
            f"SKILL.md name '{skill_name}' does not match plugin.json name '{plugin_name}'",
        )

    def test_skill_md_key_sections(self):
        """SKILL.md must contain the required rule headings."""
        required_headings = [
            "Answer first",
            "Pre-send check",
            "Persistence",
            "Rules",
        ]
        for heading in required_headings:
            with self.subTest(heading=heading):
                self.assertIn(
                    heading,
                    self.content,
                    f"Required heading not found in SKILL.md: '{heading}'",
                )

    def test_skill_md_no_empty_sections(self):
        """No ## heading should be immediately followed by another ## heading."""
        lines = self.content.splitlines()
        for i, line in enumerate(lines[:-1]):
            if line.startswith("## "):
                # Skip blank lines between headings
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines) and lines[j].startswith("## "):
                    self.fail(
                        f"Empty section detected: '{line}' is immediately followed "
                        f"by '{lines[j]}' (line {i + 1})"
                    )


class TestReadme(unittest.TestCase):
    """Tests for README.md presence and basic content."""

    def setUp(self):
        self.content = README_MD.read_text(encoding="utf-8")

    def test_readme_exists_and_nonempty(self):
        """README.md must exist and be non-empty."""
        self.assertTrue(README_MD.is_file(), f"README.md not found at {README_MD}")
        self.assertGreater(len(self.content.strip()), 0, "README.md is empty")

    def test_readme_references_skill_name(self):
        """README.md must mention 'explain-like-five'."""
        self.assertIn(
            "explain-like-five",
            self.content,
            "README.md does not reference 'explain-like-five'",
        )


class TestLicense(unittest.TestCase):
    """Tests for LICENSE file content."""

    def setUp(self):
        self.content = LICENSE_FILE.read_text(encoding="utf-8")

    def test_license_is_mit(self):
        """LICENSE must contain MIT license text."""
        self.assertIn(
            "MIT License",
            self.content,
            "LICENSE does not appear to be an MIT license",
        )
        self.assertIn(
            "Permission is hereby granted",
            self.content,
            "LICENSE is missing the MIT permission grant text",
        )


if __name__ == "__main__":
    unittest.main()
