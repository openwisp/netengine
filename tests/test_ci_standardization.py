"""Check that the test entry point accepts only supported nose2 arguments."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CiStandardizationTests(unittest.TestCase):
    def test_rejects_unsupported_arguments(self):
        for argument in (
            "--plugin=other",
            "--config=other",
            "os.system",
            "tests.test_x:TestX",
            "tests.test_dummy.test_escape",
        ):
            with self.subTest(argument=argument):
                result = subprocess.run(
                    [str(ROOT / "runtests"), argument],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("unsupported", result.stderr.lower())

    def test_allows_nested_test_labels_but_rejects_other_classes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(ROOT / "runtests", root / "runtests")
            (root / "tests" / "test_snmp").mkdir(parents=True)
            (root / "tests" / "__init__.py").touch()
            (root / "tests" / "test_snmp" / "__init__.py").touch()
            (root / "tests" / "test_snmp" / "test_probe.py").write_text(
                "import unittest\n"
                "class TestProbe(unittest.TestCase):\n    def test_ok(self): pass\n"
                "class Helper:\n    def test_bad(self): pass\n"
            )
            (root / "nose2.py").write_text(
                'import sys\ndef discover(): print("|".join(sys.argv[1:]))\n'
            )
            env = {**os.environ, "PYTHONPATH": str(root)}
            valid = subprocess.run(
                [
                    str(root / "runtests"),
                    "tests.test_snmp.test_probe.TestProbe.test_ok",
                    "-v",
                ],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
            )
            invalid = subprocess.run(
                [
                    str(root / "runtests"),
                    "tests.test_snmp.test_probe.Helper.test_bad",
                ],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(
            valid.stdout.strip(), "tests.test_snmp.test_probe.TestProbe.test_ok|-v"
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertNotIn("test_bad", invalid.stdout)

    def test_rejects_callable_in_place_of_test_module(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(ROOT / "runtests", root / "runtests")
            (root / "tests").mkdir()
            (root / "tests" / "__init__.py").write_text(
                'def test_action(): print("unexpected execution")\n'
            )
            result = subprocess.run(
                [str(root / "runtests"), "tests.test_action"],
                cwd=root,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("unexpected execution", result.stdout)
