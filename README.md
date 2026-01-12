# PMU Extractor — STRICT Skeleton

This is a strict, rule-based skeleton aligned with your global prompt:
- PHASE0..PHASE5
- Turfomania: parse only structured pages (table + pronostic + scan)
- No guessing: uncertain => empty + diagnostics
- Outputs: `resultats.txt`, `resultats.csv`, `diagnostics.csv`

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### OCR prerequisites (Turfomania boxes)
Turfomania OCR (`--tm-ocr`) relies on the system Tesseract binary. Install it with your OS
package manager, then verify:
```bash
tesseract --version
```

## Quick check (MOCK)
```bash
python main.py --date "12 janvier 2026" --reunions R1 --turfomania dummy.pdf --mock --outdir out
```

## Real run (partial implementation in this skeleton)
```bash
python main.py --date "12 janvier 2026" --reunions R1 R3 \
  --turfomania "/path/to/journal-de-turfomania-2026-01-12.pdf" \
  --veinard "/path/to/leveinard 10 jan 26.pdf" \
  --outdir out --strict
```

### Notes
- Veinard parsing is conservative stub unless you provide the **same-date** Veinard PDF.
- Paris-Turf OCR is stub: provide OCR text via `--paristurf-ocr-text`. Next step is PaddleOCR + cropping.

## Tests
```bash
python -m unittest -v
```
