from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .config import DIAG_COLUMNS
import csv

@dataclass
class DiagItem:
    reunion: str
    course: str
    nom_prix: str
    etape: str
    statut: str
    detail: str

class Diagnostics:
    def __init__(self) -> None:
        self.items: List[DiagItem] = []

    def add(self, reunion: str, course: str, nom_prix: str, etape: str, statut: str, detail: str) -> None:
        self.items.append(DiagItem(reunion, course, nom_prix, etape, statut, detail))

    def write_csv(self, path: str) -> None:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(DIAG_COLUMNS)
            for it in self.items:
                w.writerow([it.reunion, it.course, it.nom_prix, it.etape, it.statut, it.detail])
