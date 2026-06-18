"""Scoring + severity categories for HIT-6, PHQ-9, GAD-7."""

from typing import List, Tuple


def score_hit6(responses: List[int]) -> Tuple[int, str]:
    """HIT-6: 6 items, each 6/8/10/11/13. Total range 36-78."""
    if len(responses) != 6 or any(r is None for r in responses):
        return 0, "Incomplete"
    total = sum(responses)
    if total <= 49:
        cat = "Little or no impact"
    elif total <= 55:
        cat = "Some impact"
    elif total <= 59:
        cat = "Substantial impact"
    else:
        cat = "Severe impact"
    return total, cat


def score_phq9(responses: List[int]) -> Tuple[int, str]:
    """PHQ-9: 9 items, each 0-3. Total range 0-27."""
    if len(responses) != 9 or any(r is None for r in responses):
        return 0, "Incomplete"
    total = sum(responses)
    if total <= 4:
        cat = "Minimal"
    elif total <= 9:
        cat = "Mild"
    elif total <= 14:
        cat = "Moderate"
    elif total <= 19:
        cat = "Moderately severe"
    else:
        cat = "Severe"
    return total, cat


def score_gad7(responses: List[int]) -> Tuple[int, str]:
    """GAD-7: 7 items, each 0-3. Total range 0-21."""
    if len(responses) != 7 or any(r is None for r in responses):
        return 0, "Incomplete"
    total = sum(responses)
    if total <= 4:
        cat = "Minimal"
    elif total <= 9:
        cat = "Mild"
    elif total <= 14:
        cat = "Moderate"
    else:
        cat = "Severe"
    return total, cat


def phq9_suicidality_flag(responses: List[int]) -> bool:
    """Item 9 ≥ 1 means any suicidal ideation in the past 2 weeks — flag for review."""
    if len(responses) < 9 or responses[8] is None:
        return False
    return responses[8] >= 1


def change_label(baseline: float, followup: float, mcid: float) -> str:
    """Simple verdict for a follow-up vs baseline change.
    mcid = minimal clinically important difference (positive number).
    For HIT-6/PHQ-9/GAD-7, lower is better.
    """
    diff = followup - baseline
    if diff <= -mcid:
        return "Improved"
    if diff >= mcid:
        return "Worse"
    return "Unchanged"


MCID = {"HIT6": 2.5, "PHQ9": 5.0, "GAD7": 4.0}
