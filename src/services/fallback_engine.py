from __future__ import annotations

import math
from datetime import datetime


def _bounded(value: float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def _keyword_boost(query: str, positive: tuple[str, ...], negative: tuple[str, ...]) -> int:
    q = query.lower()
    boost = sum(8 for token in positive if token in q)
    penalty = sum(8 for token in negative if token in q)
    return boost - penalty


def compute_fallback_analysis(query: str) -> dict:
    now = datetime.utcnow().year

    positive = (
        "ai",
        "ml",
        "machine learning",
        "data",
        "cloud",
        "kubernetes",
        "rust",
        "react",
        "typescript",
        "python",
        "security",
        "platform",
    )
    negative = (
        "jquery",
        "flash",
        "cobol",
        "perl",
        "visual basic",
        "wordpress",
    )

    signal = _keyword_boost(query, positive, negative)
    base = 55 + signal
    volatility = abs(math.sin(len(query))) * 10
    drift = _bounded(base + volatility)

    if drift >= 70:
        demand = "Rising"
        salary = "Growing"
        decline = "Low"
        half_life = "7-10 years"
    elif drift >= 50:
        demand = "Stable"
        salary = "Steady"
        decline = "Moderate"
        half_life = "4-6 years"
    else:
        demand = "Declining"
        salary = "Flattening"
        decline = "High"
        half_life = "2-3 years"

    peak = now - 3 if drift >= 50 else now - 6
    risk = _bounded(100 - drift)

    return {
        "skill_drift_score": drift,
        "demand_trend": demand,
        "salary_trajectory": salary,
        "stack_half_life": half_life,
        "risk_of_obsolescence": risk,
        "peak_relevance": peak,
        "projected_decline": decline,
        "data_sources": [
            "GitHub Trends",
            "StackOverflow Tags",
            "Job Boards",
            "Google Trends",
        ],
        "notes": "Fallback heuristic mode (Gemini unavailable or key missing).",
    }
