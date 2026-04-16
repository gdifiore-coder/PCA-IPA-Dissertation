"""Smoke tests for the convergent integration build pipeline."""

import csv
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"
BUILD_SCRIPT = SRC_DIR / "build.py"
INVENTORY_CSV = PROJECT_DIR / "data" / "inventory.csv"
TEMPLATE = SRC_DIR / "template.html"


def build_to(output_path: Path, input_path: Path = INVENTORY_CSV) -> str:
    """Run build.py and return the generated HTML."""
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT),
         "--input", str(input_path),
         "--output", str(output_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Build failed:\n{result.stderr}")
    return output_path.read_text(encoding="utf-8")


class TestCSVParsing(unittest.TestCase):
    """Verify the source CSV is well-formed."""

    def setUp(self):
        with open(INVENTORY_CSV, newline="", encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f))

    def test_csv_readable(self):
        self.assertGreater(len(self.rows), 0, "CSV should have data rows")

    def test_required_columns_present(self):
        required = {"Code", "RQ", "Participant", "Strand", "Data_Type",
                     "Source_Tag", "Dimension", "Data_Point"}
        with open(INVENTORY_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertTrue(required.issubset(set(reader.fieldnames)),
                            f"Missing columns: {required - set(reader.fieldnames)}")

    def test_no_empty_codes(self):
        for i, row in enumerate(self.rows, start=2):
            self.assertTrue(row["Code"].strip(),
                            f"Row {i} has empty Code")

    def test_no_empty_participants(self):
        for i, row in enumerate(self.rows, start=2):
            self.assertTrue(row["Participant"].strip(),
                            f"Row {i} has empty Participant")

    def test_strand_values_valid(self):
        valid = {"QUAL", "QUANT"}
        for i, row in enumerate(self.rows, start=2):
            self.assertIn(row["Strand"].strip(), valid,
                          f"Row {i} has bad Strand: '{row['Strand']}'")

    def test_rq_code_uniqueness(self):
        seen = set()
        for i, row in enumerate(self.rows, start=2):
            key = (row["RQ"], row["Code"])
            self.assertNotIn(key, seen,
                             f"Row {i}: duplicate RQ+Code {key}")
            seen.add(key)


class TestBuildOutput(unittest.TestCase):
    """Verify the built HTML contains all expected data."""

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp()
        cls.output_path = Path(cls.tmpdir) / "test_output.html"
        cls.html = build_to(cls.output_path)
        with open(INVENTORY_CSV, newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))

    @classmethod
    def tearDownClass(cls):
        if cls.output_path.exists():
            cls.output_path.unlink()
        os.rmdir(cls.tmpdir)

    def test_all_rqs_present(self):
        rqs = sorted(set(r["RQ"] for r in self.rows))
        for rq in rqs:
            self.assertIn(f'data-rq="{rq}"', self.html,
                          f"RQ '{rq}' not found in output HTML")

    def test_all_items_present_as_elements(self):
        for row in self.rows:
            code = row["Code"]
            self.assertIn(f'data-code="{code}"', self.html,
                          f"Code '{code}' not found as element in output HTML")

    def test_all_participants_in_filter(self):
        participants = sorted(set(r["Participant"] for r in self.rows))
        for p in participants:
            self.assertIn(f'value="{p}"', self.html,
                          f"Participant '{p}' not in filter options")

    def test_item_count_matches_csv(self):
        count = self.html.count('class="item ')
        self.assertEqual(count, len(self.rows),
                         f"Expected {len(self.rows)} items, found {count}")

    def test_qual_quant_counts(self):
        qual_count = self.html.count('data-strand="QUAL"')
        quant_count = self.html.count('data-strand="QUANT"')
        expected_qual = sum(1 for r in self.rows if r["Strand"] == "QUAL")
        expected_quant = sum(1 for r in self.rows if r["Strand"] == "QUANT")
        self.assertEqual(qual_count, expected_qual)
        self.assertEqual(quant_count, expected_quant)


class TestTemplatePlaceholders(unittest.TestCase):
    """Verify no raw placeholders survive the build."""

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp()
        cls.output_path = Path(cls.tmpdir) / "test_placeholders.html"
        cls.html = build_to(cls.output_path)

    @classmethod
    def tearDownClass(cls):
        if cls.output_path.exists():
            cls.output_path.unlink()
        os.rmdir(cls.tmpdir)

    def test_no_tabs_placeholder(self):
        self.assertNotIn("{{TABS}}", self.html)

    def test_no_filter_placeholder(self):
        self.assertNotIn("{{FILTER_OPTIONS}}", self.html)

    def test_no_panels_placeholder(self):
        self.assertNotIn("{{PANELS}}", self.html)

    def test_no_rqlist_placeholder(self):
        self.assertNotIn("{{RQ_LIST}}", self.html)

    def test_no_total_placeholder(self):
        self.assertNotIn("{{TOTAL_ITEMS}}", self.html)

    def test_no_stray_double_braces(self):
        # Make sure no other {{...}} placeholders leaked through
        import re
        matches = re.findall(r"\{\{[A-Z_]+\}\}", self.html)
        self.assertEqual(matches, [],
                         f"Stray placeholders found: {matches}")


if __name__ == "__main__":
    unittest.main()
