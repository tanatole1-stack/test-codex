from __future__ import annotations
from typing import List, Tuple
import re
from .config import MAX_HORSE_NUMBER

def parse_int_tokens(text: str) -> List[str]:
    return re.findall(r"\b\d{1,2}\b", text)

def validate_num_list(nums: List[str]) -> Tuple[bool, str]:
    if not nums:
        return False, "EMPTY_LIST"
    for n in nums:
        if not n.isdigit():
            return False, f"NON_DIGIT:{n}"
        v = int(n)
        if v <= 0 or v > MAX_HORSE_NUMBER:
            return False, f"OUT_OF_RANGE:{n}"
    return True, ""

def parse_result_line(text: str) -> str:
    nums = re.findall(r"\b\d{1,2}\b", text)
    return "-".join(nums[:5]) if len(nums) >= 3 else ""

def parse_np(text: str) -> List[str]:
    return re.findall(r"\b\d{1,2}\b", text)
