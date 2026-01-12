from __future__ import annotations
import argparse, os
from pmu_extractor.pipeline import run_pipeline
from pmu_extractor.outputs import write_csv, write_txt
from pmu_extractor.config import OCR_DPI

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PMU Extractor (STRICT skeleton)")
    p.add_argument("--date", required=True, help="Date courses, e.g. '12 janvier 2026'")
    p.add_argument("--reunions", nargs="+", required=True, help="Reunions to treat, e.g. R1 R3")
    p.add_argument("--turfomania", required=True, help="Path to Turfomania PDF")
    p.add_argument("--veinard", default="", help="Path to Le Veinard PDF (optional)")
    p.add_argument("--paristurf-ocr-text", default="", help="Path to OCR text file for Paris-Turf (optional)")
    p.add_argument("--outdir", default="out", help="Output directory")
    p.add_argument("--strict", action="store_true", help="Strict mode (recommended)")
    p.add_argument("--mock", action="store_true", help="Run mock pipeline for fast validation")
    p.add_argument("--tm-ocr", action="store_true", help="Use OCR for Turfomania P/Base/Scan/C zones")
    p.add_argument("--tm-ocr-dpi", type=int, default=OCR_DPI, help="Turfomania OCR render DPI")
    return p

def main() -> None:
    args = build_argparser().parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    ocr_text = None
    if args.paristurf_ocr_text:
        with open(args.paristurf_ocr_text, "r", encoding="utf-8") as f:
            ocr_text = f.read()

    courses, diag = run_pipeline(
        date_courses=args.date,
        reunions=args.reunions,
        turfomania_pdf=args.turfomania,
        veinard_pdf=args.veinard if args.veinard else None,
        paristurf_ocr_text=ocr_text,
        strict=args.strict,
        mock=args.mock,
        tm_ocr=args.tm_ocr,
        tm_ocr_dpi=args.tm_ocr_dpi,
    )

    write_txt(os.path.join(args.outdir, "resultats.txt"), args.date, courses)
    write_csv(os.path.join(args.outdir, "resultats.csv"), courses)
    diag.write_csv(os.path.join(args.outdir, "diagnostics.csv"))

    print(f"Wrote {len(courses)} course(s) to {args.outdir}")
    print("Files: resultats.txt, resultats.csv, diagnostics.csv")

if __name__ == "__main__":
    main()
