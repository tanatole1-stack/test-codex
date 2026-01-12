from __future__ import annotations
import re

def normalize_prix_name(name: str) -> str:
    s = name.upper().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"[\.,;:!\?]", "", s)
    s = s.replace("QUINTÉ+", "QUINTE").replace("QUINTÉ", "QUINTE")
    s = s.replace("QUINTE+", "QUINTE")
    s = re.sub(r"\s+", " ", s).strip()
    return s
