#!/usr/bin/env python3
"""Build script for the convergent integration pairing tool.

Reads data/inventory.csv and injects its contents as static HTML into
src/template.html, producing dist/pairing_tool.html.
"""

import argparse
import csv
import html
import os
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "inventory.csv"
DEFAULT_OUTPUT = PROJECT_DIR / "dist" / "pairing_tool.html"
TEMPLATE_PATH = SCRIPT_DIR / "template.html"

REQUIRED_COLUMNS = {"Code", "RQ", "Participant", "Strand", "Data_Type",
                     "Source_Tag", "Dimension", "Data_Point"}


def read_inventory(path: Path) -> list[dict]:
    """Read and validate the inventory CSV."""
    rows = []
    malformed = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            print(f"ERROR: Missing columns: {missing}", file=sys.stderr)
            sys.exit(1)
        for i, row in enumerate(reader, start=2):
            issues = []
            if not row["Code"].strip():
                issues.append("empty Code")
            if not row["RQ"].strip():
                issues.append("empty RQ")
            if not row["Participant"].strip():
                issues.append("empty Participant")
            if row["Strand"].strip() not in ("QUAL", "QUANT"):
                issues.append(f"bad Strand '{row['Strand']}'")
            if issues:
                malformed.append((i, issues))
            else:
                rows.append(row)
    return rows, malformed


def build_item_html(row: dict, idx: int) -> str:
    """Render one data-point item as an HTML element."""
    code = html.escape(row["Code"])
    rq = html.escape(row["RQ"])
    participant = html.escape(row["Participant"])
    strand = row["Strand"].strip()
    data_type = html.escape(row["Data_Type"])
    source = html.escape(row["Source_Tag"])
    dimension = html.escape(row["Dimension"])
    data_point = html.escape(row["Data_Point"])

    css_class = "item qual-item" if strand == "QUAL" else "item quant-item"

    return (
        f'<div class="{css_class}" '
        f'data-code="{code}" data-rq="{rq}" data-participant="{participant}" '
        f'data-strand="{strand}" data-type="{data_type}" data-idx="{idx}">'
        f'<label>'
        f'<input type="checkbox" class="item-check" />'
        f'<span class="item-code">{code}</span> '
        f'<span class="item-participant">[{participant}]</span> '
        f'<span class="item-type">{data_type}</span>'
        f'</label>'
        f'<div class="item-dimension">{dimension}</div>'
        f'<div class="item-datapoint">{data_point}</div>'
        f'<div class="item-source">Source: {source}</div>'
        f'</div>\n'
    )


def build_html_blocks(rows: list[dict]) -> str:
    """Build the full data block: RQ tabs + item panels."""
    # Group by RQ
    by_rq = defaultdict(lambda: {"QUAL": [], "QUANT": []})
    for i, row in enumerate(rows):
        strand = row["Strand"].strip()
        by_rq[row["RQ"]][strand].append((i, row))

    rqs = sorted(by_rq.keys())
    participants = sorted(set(r["Participant"] for r in rows))

    # Build tab buttons
    tabs_html = ""
    for j, rq in enumerate(rqs):
        active = " active" if j == 0 else ""
        tabs_html += f'<button class="tab-btn{active}" data-rq="{html.escape(rq)}">{html.escape(rq)}</button>\n'

    # Build participant filter
    filter_html = '<option value="all">All Participants</option>\n'
    for p in participants:
        filter_html += f'<option value="{html.escape(p)}">{html.escape(p)}</option>\n'

    # Build panels per RQ
    panels_html = ""
    for j, rq in enumerate(rqs):
        hidden = "" if j == 0 else ' style="display:none"'
        qual_items = "".join(build_item_html(r, i) for i, r in by_rq[rq]["QUAL"])
        quant_items = "".join(build_item_html(r, i) for i, r in by_rq[rq]["QUANT"])

        panels_html += (
            f'<div class="rq-panel" data-rq="{html.escape(rq)}"{hidden}>\n'
            f'<div class="columns">\n'
            f'<div class="column qual-column">\n'
            f'<h3>QUAL — IPA Themes ({len(by_rq[rq]["QUAL"])} items)</h3>\n'
            f'{qual_items}'
            f'</div>\n'
            f'<div class="column quant-column">\n'
            f'<h3>QUANT — PCA Data ({len(by_rq[rq]["QUANT"])} items)</h3>\n'
            f'{quant_items}'
            f'</div>\n'
            f'</div>\n'
            f'</div>\n'
        )

    return tabs_html, filter_html, panels_html, rqs, participants


def print_summary(rows, malformed, rqs_list):
    """Print build summary to stdout."""
    by_rq = defaultdict(int)
    by_participant = defaultdict(int)
    by_strand_rq = defaultdict(lambda: defaultdict(int))
    for r in rows:
        by_rq[r["RQ"]] += 1
        by_participant[r["Participant"]] += 1
        by_strand_rq[r["RQ"]][r["Strand"]] += 1

    print("\n=== Build Summary ===")
    print(f"Total items: {len(rows)}")
    print()
    print("Items per RQ:")
    for rq in sorted(by_rq):
        q = by_strand_rq[rq].get("QUAL", 0)
        n = by_strand_rq[rq].get("QUANT", 0)
        print(f"  {rq}: {by_rq[rq]} total ({q} QUAL, {n} QUANT)")
    print()
    print("Items per participant:")
    for p in sorted(by_participant):
        print(f"  {p}: {by_participant[p]}")
    print()
    if malformed:
        print(f"Malformed rows skipped: {len(malformed)}")
        for line_no, issues in malformed:
            print(f"  Row {line_no}: {', '.join(issues)}")
    else:
        print("Malformed rows: 0")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Build the convergent integration pairing tool HTML."
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to inventory CSV (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Path for output HTML (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    # Read inventory
    print(f"Reading inventory from {args.input}")
    rows, malformed = read_inventory(args.input)

    if not rows:
        print("ERROR: No valid rows found.", file=sys.stderr)
        sys.exit(1)

    # Build HTML blocks
    tabs_html, filter_html, panels_html, rqs, participants = build_html_blocks(rows)

    # Read template
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: Template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Inject data
    output = template.replace("{{TABS}}", tabs_html)
    output = output.replace("{{FILTER_OPTIONS}}", filter_html)
    output = output.replace("{{PANELS}}", panels_html)
    output = output.replace("{{RQ_LIST}}", ",".join(rqs))
    output = output.replace("{{TOTAL_ITEMS}}", str(len(rows)))

    # Verify all placeholders replaced
    remaining = [p for p in ["{{TABS}}", "{{FILTER_OPTIONS}}", "{{PANELS}}",
                              "{{RQ_LIST}}", "{{TOTAL_ITEMS}}"]
                 if p in output]
    if remaining:
        print(f"ERROR: Unreplaced placeholders: {remaining}", file=sys.stderr)
        sys.exit(1)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Wrote pairing tool to {args.output}")

    # Summary
    print_summary(rows, malformed, rqs)


if __name__ == "__main__":
    main()
