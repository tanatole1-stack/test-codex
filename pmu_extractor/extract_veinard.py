from __future__ import annotations
import re
from typing import List, Tuple
import fitz
from .models import CourseRow
from .diagnostics import Diagnostics

def _find_dm(text: str) -> str:
    m = re.search(r"Derni[èe]re\s+minute[^\d]*(?:n°|No|n\s*o\s*)\s*(\d{1,2})", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""

def _find_rp(text: str) -> str:
    m = re.search(r"Rep[ée]r[ée]\s+sur\s+les\s+pistes[\s\S]{0,140}?(?:n°|No|n\s*o\s*)\s*(\d{1,2})", text, flags=re.IGNORECASE)
    return m.group(1) if m else ""

def extract_veinard(pdf_path: str, courses: List[CourseRow], diag: Diagnostics) -> None:
    doc = fitz.open(pdf_path)
    full_text = "\n\n".join(doc.load_page(i).get_text("text") for i in range(doc.page_count))
    dm = _find_dm(full_text)
    rp = _find_rp(full_text)

    for c in courses:
        # Conservative: only DM/RP, because the provided Veinard PDF is not same date as Turfomania.
        if dm and not c.v_dm:
            c.v_dm = dm
        if rp and not c.v_rp:
            c.v_rp = rp
        diag.add(c.reunion, c.course, c.nom_prix, "PHASE2", "VEINARD_TODO",
                 "Need same-date Veinard PDF to implement strict NomPrix matching + JeChoisis/Outsiders")
