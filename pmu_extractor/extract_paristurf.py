from __future__ import annotations
import re
from typing import List, Tuple
from .models import CourseRow
from .diagnostics import Diagnostics
from .quality import validate_num_list

def parse_notre_choix(text: str) -> Tuple[List[str], List[str]]:
    t = text.upper()
    m = re.search(r"NOTRE\s+CHOIX\s*:?\s*(.+)", t)
    if not m:
        return [], []
    tail = m.group(1)
    nums = re.findall(r"\b\d{1,2}\b", tail)
    if len(nums) < 2:
        return [], []
    first2 = nums[:2]
    rest = nums[2:]
    ok1, _ = validate_num_list(first2)
    ok2, _ = validate_num_list(rest) if rest else (True, "")
    if ok1 and ok2:
        return first2, rest
    return [], []

def extract_paristurf_from_ocr_text(ocr_text: str, courses: List[CourseRow], diag: Diagnostics) -> None:
    jc, outs = parse_notre_choix(ocr_text)
    for c in courses:
        if jc:
            c.pt_jechoisis = jc
            c.pt_outsiders = outs
        else:
            diag.add(c.reunion, c.course, c.nom_prix, "PHASE3", "PT_OCR_UNCERTAIN",
                     "NOTRE CHOIX not parsed from OCR text")
# TODO: implement PaddleOCR + preprocessing + crop NOTRE CHOIX zone for production.
