from __future__ import annotations
import re
from typing import List, Tuple
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from .models import CourseRow
from .diagnostics import Diagnostics
from .config import TM_STRUCTURED_A_HEADERS, TM_STRUCTURED_B_KEYS, TM_STRUCTURED_C_KEYS
from .quality import parse_int_tokens, validate_num_list

ZONE_P = (0.03, 0.62, 0.45, 0.92)
ZONE_BASE = (0.45, 0.62, 0.65, 0.92)
ZONE_SCAN = (0.65, 0.62, 0.97, 0.92)
ZONE_C = (0.02, 0.05, 0.12, 0.12)

def _page_to_image(page: fitz.Page, dpi: int) -> Image.Image:
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

def _zone_rect(page: fitz.Page, zone: tuple[float, float, float, float]) -> fitz.Rect:
    x0, y0, x1, y1 = zone
    return fitz.Rect(
        page.rect.x0 + page.rect.width * x0,
        page.rect.y0 + page.rect.height * y0,
        page.rect.x0 + page.rect.width * x1,
        page.rect.y0 + page.rect.height * y1,
    )

def _crop_zone(img: Image.Image, rect: fitz.Rect, dpi: int) -> Image.Image:
    scale = dpi / 72.0
    box = (
        int(rect.x0 * scale),
        int(rect.y0 * scale),
        int(rect.x1 * scale),
        int(rect.y1 * scale),
    )
    return img.crop(box)

def _ocr_text(img: Image.Image, psm: int = 6) -> str:
    cfg = f"--psm {psm} -c tessedit_char_whitelist=0123456789"
    return pytesseract.image_to_string(img, config=cfg)

def _digits_only(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return re.fullmatch(r"[0-9\s]+", stripped) is not None

def _parse_ocr_numbers(text: str) -> List[str]:
    if not _digits_only(text):
        return []
    nums = parse_int_tokens(text)
    ok, _ = validate_num_list(nums) if nums else (False, "EMPTY")
    return nums if ok else []

def is_structured_page(text: str) -> bool:
    t = text.upper()
    a = sum(1 for k in TM_STRUCTURED_A_HEADERS if k in t) >= 2
    b = any(k in t for k in TM_STRUCTURED_B_KEYS)
    c = any(k in t for k in TM_STRUCTURED_C_KEYS)
    return (a + b + c) >= 2

def parse_reunion_course(text: str) -> Tuple[str, str]:
    m = re.search(r"\(\s*R[ÉE]UNION\s*(\d+)\s*[-–]\s*Course\s*(\d+)\s*\)", text, flags=re.IGNORECASE)
    if m:
        return f"R{m.group(1)}", f"C{m.group(2)}"
    m2 = re.search(r"\bR(\d)\s*C(\d{1,2})\b", text, flags=re.IGNORECASE)
    if m2:
        return f"R{m2.group(1)}", f"C{m2.group(2)}"
    return "", ""

def parse_nom_prix(text: str) -> str:
    for ln in (ln.strip() for ln in text.splitlines()):
        if re.match(r"^PRIX\s+", ln, flags=re.IGNORECASE):
            return ln
    return ""

def parse_caracteristiques(text: str) -> str:
    for ln in (ln.strip() for ln in text.splitlines() if ln.strip()):
        if "MÈT" in ln.upper() or "METRES" in ln.upper():
            return ln
    return ""

def parse_partants(text: str) -> str:
    m = re.search(r"\b(\d{1,2})\s+partants\b", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""

def parse_montant(text: str) -> str:
    m = re.search(r"(\d[\d\s\.]{2,})\s*(€|EUROS)", text, flags=re.IGNORECASE)
    if not m:
        return ""
    val = m.group(1).replace(" ", "").replace(".", "")
    return f"{val}€"

def _block(text: str, anchor: str, max_lines: int = 10) -> str:
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if anchor.upper() in ln.upper():
            return "\n".join(lines[i:i+max_lines])
    return ""

def parse_pronostic(text: str) -> List[str]:
    blk = _block(text, "PRONOSTIC DE TURFOMANIA", 8)
    nums = parse_int_tokens(blk)
    if len(nums) > 12:
        nums = nums[:8]
    ok, _ = validate_num_list(nums) if nums else (False, "EMPTY")
    return nums if ok else []

def parse_base(text: str) -> str:
    m = re.search(r"BASE\s*:\s*(\d{1,2})\b", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""

def parse_trouble_fete(text: str) -> str:
    m = re.search(r"TROUBLE\s*[-–]?\s*F[ÊE]TE\s*:?\s*(\d{1,2})\b", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""

def parse_scan(text: str) -> List[str]:
    blk = _block(text, "SCAN PREMIUM", 10)
    nums = parse_int_tokens(blk)
    if len(nums) > 14:
        nums = nums[:8]
    ok, _ = validate_num_list(nums) if nums else (False, "EMPTY")
    return nums if ok else []

def extract_turfomania(pdf_path: str,
                       reunions_to_keep: List[str],
                       diag: Diagnostics,
                       strict: bool = True,
                       tm_ocr: bool = False,
                       tm_ocr_dpi: int = 350) -> List[CourseRow]:
    doc = fitz.open(pdf_path)
    structured = []
    for pno in range(doc.page_count):
        txt = doc.load_page(pno).get_text("text")
        if is_structured_page(txt):
            structured.append(pno)

    rows: List[CourseRow] = []
    for pno in structured:
        page = doc.load_page(pno)
        txt = page.get_text("text")
        r, c = parse_reunion_course(txt)
        nom = parse_nom_prix(txt)

        if not r and len(reunions_to_keep) == 1:
            r = reunions_to_keep[0]
        if not r and len(reunions_to_keep) > 1:
            diag.add(r, c, nom, "PHASE1", "TM_NO_REUNION", f"Page {pno+1}: Reunion not found (multi skip)")
            continue

        if r and reunions_to_keep and r not in reunions_to_keep:
            continue
        if strict and not r:
            diag.add(r, c, nom, "PHASE1", "TM_NO_REUNION", f"Page {pno+1}: Reunion not found (strict skip)")
            continue

        row = CourseRow(
            reunion=r,
            course=c,
            nom_prix=nom,
            caracteristiques=parse_caracteristiques(txt),
            partants=parse_partants(txt),
            montant=parse_montant(txt),
        )
        if tm_ocr:
            diag.add(r, c, nom, "PHASE1", "TM_OCR_USED", f"Page {pno+1}: OCR enabled")
            img = _page_to_image(page, tm_ocr_dpi)
            rect_p = _zone_rect(page, ZONE_P)
            rect_base = _zone_rect(page, ZONE_BASE)
            rect_scan = _zone_rect(page, ZONE_SCAN)
            rect_c = _zone_rect(page, ZONE_C)

            ocr_c = _ocr_text(_crop_zone(img, rect_c, tm_ocr_dpi), psm=7)
            nums_c = _parse_ocr_numbers(ocr_c)
            if len(nums_c) == 1:
                row.course = f"C{nums_c[0]}"
            else:
                row.course = ""
                diag.add(r, c, nom, "PHASE1", "TM_OCR_FAIL_C", f"Page {pno+1}: OCR course invalid")
            c = row.course

            ocr_p = _ocr_text(_crop_zone(img, rect_p, tm_ocr_dpi), psm=6)
            nums_p = _parse_ocr_numbers(ocr_p)
            if len(nums_p) >= 4:
                row.tm_p = nums_p
            else:
                row.tm_p = []
                diag.add(r, c, nom, "PHASE1", "TM_OCR_FAIL_P", f"Page {pno+1}: OCR pronostic invalid")

            ocr_base = _ocr_text(_crop_zone(img, rect_base, tm_ocr_dpi), psm=7)
            nums_base = _parse_ocr_numbers(ocr_base)
            if len(nums_base) == 1:
                row.tm_b = nums_base[0]
            else:
                row.tm_b = ""
                diag.add(r, c, nom, "PHASE1", "TM_OCR_FAIL_BASE", f"Page {pno+1}: OCR base invalid")

            ocr_scan = _ocr_text(_crop_zone(img, rect_scan, tm_ocr_dpi), psm=6)
            nums_scan = _parse_ocr_numbers(ocr_scan)
            if len(nums_scan) >= 4:
                row.tm_scan = nums_scan
            else:
                row.tm_scan = []
                diag.add(r, c, nom, "PHASE1", "TM_OCR_FAIL_SCAN", f"Page {pno+1}: OCR scan invalid")
        else:
            row.tm_p = parse_pronostic(txt)
            if not row.tm_p:
                diag.add(r, c, nom, "PHASE1", "TM_P_EMPTY", f"Page {pno+1}: Pronostic not parsed")
            row.tm_b = parse_base(txt)
            if not row.tm_b:
                diag.add(r, c, nom, "PHASE1", "TM_BASE_EMPTY", f"Page {pno+1}: BASE not found")
            row.tm_scan = parse_scan(txt)
            if not row.tm_scan:
                diag.add(r, c, nom, "PHASE1", "TM_SCAN_EMPTY", f"Page {pno+1}: SCAN not parsed")

        row.tm_t = parse_trouble_fete(txt)

        rows.append(row)

    return rows
