from __future__ import annotations
from typing import List
from .models import CourseRow
from .config import CSV_COLUMNS
import csv

def _join(nums: List[str]) -> str:
    return ";".join(nums) if nums else ""

def write_csv(path: str, rows: List[CourseRow]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLUMNS)
        for r in rows:
            w.writerow([
                r.reunion, r.hippodrome, r.course, r.nom_prix, r.caracteristiques, r.partants, r.montant,
                _join(r.tm_p), _join(r.tm_p_rouges), r.tm_b, r.tm_t, _join(r.tm_scan), _join(r.tm_scan_rouges),
                _join(r.v_jechoisis), _join(r.v_outsiders), r.v_dm, r.v_rp,
                _join(r.pt_jechoisis), _join(r.pt_outsiders),
                r.resultat, _join(r.non_partants),
            ])

def _fmt_list(prefix: str, nums: List[str]) -> str:
    return f"{prefix}({','.join(nums)})" if nums else f"{prefix}()"

def write_txt(path: str, date_courses: str, rows: List[CourseRow]) -> None:
    lines = [f"Pronostics et Résultats du {date_courses}", ""]
    from collections import defaultdict
    by_r = defaultdict(list)
    for r in rows:
        by_r[r.reunion or "R?"].append(r)

    for reunion in sorted(by_r.keys()):
        hippo = by_r[reunion][0].hippodrome if by_r[reunion] else ""
        lines.append(f"## {reunion} – {hippo}".rstrip())
        for r in by_r[reunion]:
            lines.append(f"### {r.course or 'C?'} – {r.nom_prix}")
            lines.append(f"Caractéristiques: {r.caracteristiques}".rstrip())
            lines.append(f"Partants: {r.partants}".rstrip())
            lines.append(_fmt_list("P", r.tm_p))
            lines.append(f"B({r.tm_b})" if r.tm_b else "B()")
            lines.append(f"T({r.tm_t})" if r.tm_t else "T()")
            lines.append(_fmt_list("Scan", r.tm_scan))
            v = f"V({','.join(r.v_jechoisis)})" if r.v_jechoisis else "V()"
            if r.v_outsiders:
                v += f"({','.join(r.v_outsiders)})"
            v += f" DM({r.v_dm})" if r.v_dm else " DM()"
            v += f" RP({r.v_rp})" if r.v_rp else " RP()"
            lines.append(v.strip())
            pt = f"PT({','.join(r.pt_jechoisis)})" if r.pt_jechoisis else "PT()"
            if r.pt_outsiders:
                pt += f"({','.join(r.pt_outsiders)})"
            lines.append(pt)
            lines.append(f"R({r.resultat})" if r.resultat else "R()")
            lines.append(_fmt_list("NP", r.non_partants))
            lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
