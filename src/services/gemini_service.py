from __future__ import annotations

import json
import re
from typing import Any

from google import genai

from src.config import settings
from src.services.fallback_engine import compute_fallback_analysis


PROMPT_TEMPLATE = """
You are a labor-market analyst AI for software engineering skills.
Given a target query (tech stack OR job title), estimate:
- demand trend (Rising/Stable/Declining)
- salary trajectory
- stack half-life
- risk of obsolescence score (0-100, where 100 means very high risk)
- skill drift score (0-100, where 100 means very strong long-term relevance)
- peak relevance year
- projected decline (Low/Moderate/High)

Use this context of data sources conceptually:
GitHub Trends, StackOverflow tags, Job boards, Google Trends.

Return ONLY valid JSON with keys exactly:
query, skill_drift_score, demand_trend, salary_trajectory, stack_half_life,
risk_of_obsolescence, peak_relevance, projected_decline, explanation, confidence.

confidence must be one of: low, medium, high.

Target query: {query}
""".strip()


class GeminiSkillDriftService:
    def __init__(self) -> None:
        self.model = settings.gemini_model
        self.api_key = settings.gemini_api_key

    def analyze(self, query: str) -> dict[str, Any]:
        if not self.api_key:
            result = compute_fallback_analysis(query)
            result["query"] = query
            return result

        client = genai.Client(api_key=self.api_key)
        prompt = PROMPT_TEMPLATE.format(query=query)

        try:
            response = client.models.generate_content(model=self.model, contents=prompt)
            raw_text = response.text or ""
            parsed = self._parse_json(raw_text)
            parsed.setdefault("query", query)
            parsed.setdefault("confidence", "medium")
            parsed.setdefault("data_sources", [
                "GitHub Trends",
                "StackOverflow Tags",
                "Job Boards",
                "Google Trends",
            ])
            return parsed
        except Exception:
            result = compute_fallback_analysis(query)
            result["query"] = query
            return result

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Gemini returned empty response")

        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?", "", text).strip()
            text = re.sub(r"```$", "", text).strip()

        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("Gemini response is not a JSON object")
        return data
