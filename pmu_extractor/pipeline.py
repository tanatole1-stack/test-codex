from __future__ import annotations
from typing import List, Optional
from .diagnostics import Diagnostics
from .models import CourseRow
from .extract_turfomania import extract_turfomania
from .extract_veinard import extract_veinard
from .extract_paristurf import extract_paristurf_from_ocr_text
from .extract_genybet import extract_genybet

def run_pipeline(date_courses: str,
                 reunions: List[str],
                 turfomania_pdf: str,
                 veinard_pdf: str | None,
                 paristurf_ocr_text: str | None,
                 strict: bool = True,
                 mock: bool = False,
                 tm_ocr: bool = False,
                 tm_ocr_dpi: int = 350) -> tuple[list[CourseRow], Diagnostics]:
    diag = Diagnostics()

    if mock:
        r = CourseRow(
            reunion=reunions[0] if reunions else "R1",
            hippodrome="CAGNES SUR MER",
            course="C2",
            nom_prix="PRIX VANS BARBOT (PRIX DU LANGUEDOC)",
            caracteristiques="Plat - Handicap divise Classe 2 - 4 ans et Plus - 1600 mètres - (PSF), Corde à gauche - Ref: +19 - départ vers 13h55",
            partants="16",
            montant="50900€",
            tm_p=["5","12","1","9","2","6","15","4"],
            tm_b="1",
            tm_scan=["5","9","16","12","2","7","15","10"],
        )
        return [r], diag

    courses = extract_turfomania(
        turfomania_pdf,
        reunions,
        diag,
        strict=strict,
        tm_ocr=tm_ocr,
        tm_ocr_dpi=tm_ocr_dpi,
    )
    if veinard_pdf:
        extract_veinard(veinard_pdf, courses, diag)
    if paristurf_ocr_text:
        extract_paristurf_from_ocr_text(paristurf_ocr_text, courses, diag)

    extract_genybet(courses, diag)
    return courses, diag
