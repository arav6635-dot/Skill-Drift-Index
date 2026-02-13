# Skill Drift Index (Python + Flask + Gemini 2.5 Flash)

Backend API that accepts a tech stack or job title and returns:
- demand trend
- salary trajectory
- stack half-life
- risk of obsolescence
- skill drift score
- peak relevance and projected decline

## 1) Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Environment

A separate `.env` file is already included. Update it with your Gemini key:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=5001
FLASK_ENV=development
```

## 3) Run

```bash
python run.py
```

## 4) Web UI

Open in browser:

```bash
http://localhost:5001/
```

## 5) API

### Health check

```bash
curl http://localhost:5001/health
```

### Analyze skill drift

```bash
curl -X POST http://localhost:5001/api/skill-drift/analyze \
  -H "Content-Type: application/json" \
  -d '{"tech_stack":"React, Django, Rust"}'
```

or

```bash
curl -X POST http://localhost:5001/api/skill-drift/analyze \
  -H "Content-Type: application/json" \
  -d '{"job_title":"Frontend Engineer"}'
```

## Notes

- If `GEMINI_API_KEY` is missing or Gemini call fails, the app uses a deterministic fallback scoring engine.
- Gemini response is constrained to JSON for easier frontend integration.
- API metadata endpoint: `GET /api`
# Skill-Drift-Index
