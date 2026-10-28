"""Tests for prompt_expander.cli end-to-end expansion."""

import json
import os
import tempfile
import unittest

from prompt_expander.cli import expand, main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.template = os.path.join(self.tmp, "template.txt")
        with open(self.template, "w", encoding="utf-8") as handle:
            handle.write("Dear {{name}},\nWelcome to {{place}}.\n")

    def _write_csv(self, rows):
        import csv

        path = os.path.join(self.tmp, "data.csv")
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["name", "place"])
            writer.writeheader()
            writer.writerows(rows)
        return path

    def _write_json(self, data):
        path = os.path.join(self.tmp, "data.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        return path

    def test_csv_writes_files(self):
        data_path = self._write_csv(
            [{"name": "Dylan", "place": "Indiana"}, {"name": "Sam", "place": "Ohio"}]
        )
        results = expand(self.template, data_path, out_dir=os.path.join(self.tmp, "out"))
        self.assertEqual(len(results), 2)
        self.assertEqual([r[0] for r in results], ["Dylan.txt", "Sam.txt"])
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "out", "Dylan.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "out", "Sam.txt")))
        with open(os.path.join(self.tmp, "out", "Dylan.txt"), encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "Dear Dylan,\nWelcome to Indiana.\n")

    def test_csv_uses_name_column(self):
        data_path = self._write_csv(
            [{"name": "Dylan", "place": "Indiana"}, {"name": "Sam", "place": "Ohio"}]
        )
        results = expand(self.template, data_path, out_dir=os.path.join(self.tmp, "out"))
        self.assertEqual([r[0] for r in results], ["Dylan.txt", "Sam.txt"])

    def test_json_list(self):
        data_path = self._write_json(
            [{"name": "Dylan", "place": "Indiana"}, {"name": "Sam", "place": "Ohio"}]
        )
        results = expand(self.template, data_path, out_dir=os.path.join(self.tmp, "out"))
        self.assertEqual(len(results), 2)
        self.assertEqual([r[0] for r in results], ["Dylan.txt", "Sam.txt"])
        with open(os.path.join(self.tmp, "out", "Dylan.txt"), encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "Dear Dylan,\nWelcome to Indiana.\n")

    def test_json_single_object(self):
        data_path = self._write_json({"name": "Dylan", "place": "Indiana"})
        results = expand(self.template, data_path, out_dir=os.path.join(self.tmp, "out"))
        self.assertEqual(len(results), 1)

    def test_dry_run_writes_nothing(self):
        data_path = self._write_csv([{"name": "Dylan", "place": "Indiana"}])
        results = expand(
            self.template, data_path, out_dir=os.path.join(self.tmp, "out"), dry_run=True
        )
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "out")))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Dear Dylan,\nWelcome to Indiana.\n")

    def test_main_exits_zero(self):
        data_path = self._write_csv([{"name": "Dylan", "place": "Indiana"}])
        out = os.path.join(self.tmp, "out")
        self.assertEqual(
            main(["--template", self.template, "--data", data_path, "--out", out]), 0
        )
        self.assertTrue(os.path.exists(os.path.join(out, "Dylan.txt")))

    def test_unsupported_extension_raises(self):
        bad = os.path.join(self.tmp, "data.txt")
        open(bad, "w").close()
        with self.assertRaises(ValueError):
            expand(self.template, bad)


if __name__ == "__main__":
    unittest.main()
