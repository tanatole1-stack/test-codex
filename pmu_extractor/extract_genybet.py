from __future__ import annotations
from typing import List
from .models import CourseRow
from .diagnostics import Diagnostics

def extract_genybet(courses: List[CourseRow], diag: Diagnostics) -> None:
    for c in courses:
        diag.add(c.reunion, c.course, c.nom_prix, "PHASE4", "GENYBET_TODO",
                 "Implement strict matching + result/NP extraction")
