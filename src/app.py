from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from src.config import settings
from src.services.gemini_service import GeminiSkillDriftService

app = Flask(__name__)
service = GeminiSkillDriftService()


@app.get("/")
def index() -> str:
    return render_template("index.html")

@app.get("/api")
def api_info() -> tuple:
    return (
        jsonify(
            {
                "service": "Skill Drift Index API",
                "status": "running",
                "endpoints": {
                    "health": "GET /health",
                    "analyze": "POST /api/skill-drift/analyze",
                },
                "example_payload": {
                    "query": "React, Django, Rust",
                    "job_title": "Frontend Engineer",
                },
            }
        ),
        200,
    )


@app.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok", "service": "skill-drift-index"}), 200


@app.post("/api/skill-drift/analyze")
def analyze_skill_drift() -> tuple:
    payload = request.get_json(silent=True) or {}

    query = (
        payload.get("query")
        or payload.get("tech_stack")
        or payload.get("job_title")
        or ""
    ).strip()

    if not query:
        return (
            jsonify(
                {
                    "error": "Missing input. Provide one of: query, tech_stack, or job_title"
                }
            ),
            400,
        )

    result = service.analyze(query)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.port, debug=settings.flask_env == "development")
