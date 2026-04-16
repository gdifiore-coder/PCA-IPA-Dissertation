# Convergent Integration Pairing Tool

A self-contained HTML tool for the integration phase of a convergent mixed-methods dissertation combining Interpretative Phenomenological Analysis (IPA) with Principal Component Analysis (PCA).

## Methodology

This tool implements the **two-pass convergent integration workflow** described in Creswell and Plano Clark (2018):

- **Pass 1 (qual-driven):** Work through qualitative data points one at a time, finding quantitative counterparts. Each qualitative item is either paired with one or more quantitative items (**PAIR**) or marked as having no quantitative match (**SILENT(Q)**).
- **Pass 2 (quant sweep):** Review remaining unpaired quantitative items. Each can be attached to an existing pair that was missed in Pass 1 (**ATTACH**) or marked as having no qualitative counterpart (**SILENT(N)**).

Classification of the pairings (convergent, divergent, expansion, etc.) happens in a separate step. This tool produces only the pairings themselves.

## Project structure

```
convergent-integration/
├── data/
│   ├── inventory.csv          Source-of-truth data point inventory
│   └── pairings/              Exported pairing CSVs (audit trail)
├── src/
│   ├── build.py               Reads CSV, injects data into template, writes HTML
│   └── template.html          HTML shell with {{PLACEHOLDER}} markers
├── dist/
│   └── pairing_tool.html      Built artifact (gitignored)
├── tests/
│   └── test_build.py          Smoke tests
├── .gitignore
├── README.md
└── requirements.txt
```

## Workflow

### 1. Update the inventory

Edit `data/inventory.csv`. Required columns: `Code`, `RQ`, `Participant`, `Strand` (QUAL or QUANT), `Data_Type`, `Source_Tag`, `Dimension`, `Data_Point`. The combination of `RQ` + `Code` must be unique across all rows.

### 2. Rebuild the tool

```bash
cd convergent-integration
python src/build.py
```

Optional flags:

```
python src/build.py --input path/to/other.csv --output path/to/output.html
```

The build prints a summary showing item counts per RQ, per participant, and any malformed rows that were skipped.

### 3. Open the pairing tool

Open `dist/pairing_tool.html` in any modern browser (Chrome on Chromebook, Boox browser, etc.). The file is fully self-contained — no server required, works offline.

### 4. Pair items

- Use the **RQ tabs** to switch between research questions.
- Use the **participant filter** to narrow both columns.
- In **Pass 1**: select a qualitative item on the left, select matching quantitative items on the right, click **PAIR**. Use **SILENT(Q)** for qual items with no quant match.
- In **Pass 2**: click an existing pair in the pairings panel to target it, select unpaired quant items, click **ATTACH**. Use **SILENT(N)** for quant items with no qual match.
- Paired items gray out and cannot be double-paired.
- Pairings persist in `localStorage` across browser sessions.

### 5. Export and commit

Click **EXPORT CSV** to download a `pairings_YYYY-MM-DD.csv` file. Move it into `data/pairings/` and commit for an audit trail:

```bash
cp ~/Downloads/pairings_2026-04-16.csv data/pairings/
git add data/pairings/pairings_2026-04-16.csv
git commit -m "Add pairings export 2026-04-16"
```

### Export format

| Column | Description |
|--------|-------------|
| RQ | Research question (RQ1a, RQ1b, RQ2, RQ3) |
| Pair# | Pair identifier (P1, P2, ...) |
| Type | `pair`, `silent-qual`, or `silent-quant` |
| Qual_Codes | Semicolon-separated qualitative codes |
| Quant_Codes | Semicolon-separated quantitative codes |

## Running tests

```bash
cd convergent-integration
python -m unittest tests.test_build -v
```

## Dependencies

None beyond Python 3.8+ standard library. No pip install needed.
