from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CourseRow:
    reunion: str = ""
    hippodrome: str = ""
    course: str = ""     # "C2"
    nom_prix: str = ""
    caracteristiques: str = ""
    partants: str = ""
    montant: str = ""
    heure: str = ""

    tm_p: List[str] = field(default_factory=list)
    tm_p_rouges: List[str] = field(default_factory=list)
    tm_b: str = ""
    tm_t: str = ""
    tm_scan: List[str] = field(default_factory=list)
    tm_scan_rouges: List[str] = field(default_factory=list)

    v_jechoisis: List[str] = field(default_factory=list)
    v_outsiders: List[str] = field(default_factory=list)
    v_dm: str = ""
    v_rp: str = ""

    pt_jechoisis: List[str] = field(default_factory=list)
    pt_outsiders: List[str] = field(default_factory=list)

    resultat: str = ""     # "12-5-1-3-8"
    non_partants: List[str] = field(default_factory=list)

    meta: Dict[str, str] = field(default_factory=dict)
