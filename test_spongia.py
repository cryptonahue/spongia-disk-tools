import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import spongia


class SpongiaTests(unittest.TestCase):
    def test_parse_size(self):
        self.assertEqual(spongia.parse_size("1KB"), 1024)
        self.assertEqual(spongia.parse_size("1.5MB"), int(1.5 * 1024 ** 2))
        self.assertEqual(spongia.parse_size("42"), 42)

    def test_confirm_si_by_language(self):
        self.assertTrue(spongia.confirm_si("sí", "es"))
        self.assertTrue(spongia.confirm_si("yes", "en"))
        self.assertFalse(spongia.confirm_si("sim", "en"))

    def test_remove_file_permanently_when_forced(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "temporary.txt"
            target.write_text("temporary", encoding="utf-8")
            result = spongia.remove_path(
                target, to_trash=False, force=True,
                protected_dirs=[], lang="en"
            )
            self.assertEqual(result, 0)
            self.assertFalse(target.exists())

    def test_remove_rejects_protected_descendant(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "protected.txt"
            target.write_text("protected", encoding="utf-8")
            result = spongia.remove_path(
                target, to_trash=False, force=True,
                protected_dirs=[root], lang="en"
            )
            self.assertEqual(result, 1)
            self.assertTrue(target.exists())

    def test_remove_directory_requires_recursive(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "folder"
            target.mkdir()
            result = spongia.remove_path(
                target, to_trash=False, force=True,
                protected_dirs=[], lang="en"
            )
            self.assertEqual(result, 1)
            self.assertTrue(target.exists())

    def test_remove_symlink_removes_link_not_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            link = root / "link.txt"
            original.write_text("keep", encoding="utf-8")
            try:
                link.symlink_to(original)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks are unavailable in this environment")

            result = spongia.remove_path(
                link, to_trash=False, force=True,
                protected_dirs=[], lang="en"
            )
            self.assertEqual(result, 0)
            self.assertFalse(link.exists())
            self.assertTrue(original.exists())

    def test_parse_size_rejects_unknown_unit(self):
        with self.assertRaises(ValueError):
            spongia.parse_size("10XB")


if __name__ == "__main__":
    unittest.main()
