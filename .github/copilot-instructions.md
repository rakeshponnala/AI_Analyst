<!-- Copilot / AI agent guidance for HedgeAI repository -->
# HedgeAI — Copilot instructions

This file captures the essential, repository-specific guidance an AI coding agent needs to be immediately productive.

**Quick Context**
- **Backend:** FastAPI app in `backend/` (entry: `backend/main.py`).
- **Frontend:** Next.js app in `frontend/` (entry via `frontend/package.json`).
- **AI:** Uses Anthropic (`anthropic` package) in `app/services/analysis_service.py`.

**What this project wants from AI agents (high level)**
- Implement and change code while preserving the strict AI prompt/data rules in `AnalysisService.SYSTEM_PROMPT` (see `backend/app/services/analysis_service.py`).
- Avoid changing the analysis formatting and the CRITICAL DATA ACCURACY RULES — those are deliberate constraints: the model must only use exact numbers provided.

**Architecture & key files** (read these before modifying behavior)
- `backend/main.py` — FastAPI app bootstrap, logging + CORS configuration, router include.
- `backend/app/api/routes.py` — All HTTP endpoints. The `analyze_stock` endpoint calls `TickerService` and `AnalysisService` and returns `AnalysisResponse`.
- `backend/app/services/analysis_service.py` — Constructs the AI prompt, calls Anthropic, extracts the `rating` and returns the structured response.
- `backend/app/services/data_service.py` — Fetches stock data (`yfinance`) and news (`ddgs`), formats values used in prompts (numbers are rounded/formatted here). Changes here affect what the AI can cite.
- `backend/app/services/ticker_service.py` — Dictionary-driven company-name → ticker mapping. Add common names here when needed.
- `backend/app/models/schemas.py` — Pydantic models used by FastAPI; keep response shapes in sync with `routes.py` and `AnalysisService` return values.
- `backend/app/core/config.py` — Environment-driven settings (API keys, model id, tokens, temperature). Do not hard-code API keys.
- `backend/app/core/logging_config.py` — Centralized logging; logs are written to `logs/hedgeai.log`.

**Developer workflows & run commands**
- Backend (uses the provided venv at `backend/env` if present):
  - Activate: `source backend/env/bin/activate` (macOS / zsh)
  - Install: `pip install -r backend/requirements.txt`
  - Run dev server: `uvicorn main:app --reload` or `python backend/main.py` (the file calls uvicorn when executed).
  - API docs: `http://127.0.0.1:8000/docs` and `/redoc`.
- Frontend:
  - `cd frontend && npm install`
  - `npm run dev` → `http://localhost:3000`

**Important conventions and patterns (do not break these)**
- Prompt integrity: `AnalysisService.SYSTEM_PROMPT` contains explicit grammar and data-accuracy rules. Do not alter wording that mandates "ONLY use the EXACT numbers provided" or the required output format (SUMMARY / KEY RISKS / VERDICT). Tests and UI expect that exact structure.
- Exact-number usage: `DataService` formats and rounds numbers before building the `user_message`. The AI must not invent or reformat numbers — keep numeric strings consistent between `data_service` and `analysis_service`.
- Verdict extraction: `AnalysisService._extract_rating` looks for phrases like `"verdict: bearish"` or `**bearish**`. If you change the output format, also update `_extract_rating` and `schemas.AnalysisResponse` accordingly.
- Ticker resolution: `TickerService.resolve_ticker` prioritizes `COMPANY_TO_TICKER`. To support more company-name inputs, add lowercased keys to that dict (see many examples in the file).
- Error handling: Routes raise `HTTPException` for client/server errors. If an agent changes error responses, ensure API contract (status codes / response models) remains compatible.

**Integration points & external dependencies**
- Anthropic client — used in `analysis_service.py`. The Anthropic API key must be set in env: `ANTHROPIC_API_KEY`.
- Yahoo Finance (`yfinance`) — used in `data_service.py` to pull price and financials.
- DuckDuckGo news (`ddgs`) — used to collect headlines for the prompt.

**Guidance for making changes**
- When editing the AI prompt or response parsing:
  - Update `AnalysisService.SYSTEM_PROMPT` and `USER_PROMPT_TEMPLATE` together.
  - Update `_extract_rating` to match any new verdict wording.
  - Run the backend locally and exercise `GET /api/analyze/{ticker}` to verify the AI output shape.
- When changing what fields are present in responses, update `backend/app/models/schemas.py` first and then propagate changes to `routes.py` and any frontend consumption points.
- Use `get_logger(__name__)` for module logging instead of `print` where possible; many modules already use `get_logger`.

**Example quick tasks (how an agent should implement them)**
- Add a new company mapping: edit `backend/app/services/ticker_service.py` → add `"company name": "TICKER"` (lowercase key).
- Increase news count: change `NEWS_MAX_RESULTS` in `backend/app/core/config.py` (or `.env`) and ensure the prompt formatting still fits `AI_MAX_TOKENS`.
- Change model or tokens: update `AI_MODEL_NAME` / `AI_MAX_TOKENS` in `.env` or `config.py`. Verify Anthropic client call in `AnalysisService` uses these settings.

**Where tests / CI hooks would be added**
- This repo currently has no test harness. If you add tests, place them under `backend/tests/` and use a small matrix in CI that:
  - Boots a venv, installs `requirements.txt`
  - Runs a unit test that mocks the Anthropic client and yfinance calls

**If you get stuck / quick checks**
- If analysis returns unexpected text, inspect `logs/hedgeai.log` (configured by `logging_config.py`).
- If failures are due to missing API keys, check `backend/.env` and `backend/app/core/config.py`.

---
If anything here looks incomplete or you want me to expand a section (example prompts, mock responses for unit tests, or suggested CI steps), tell me which section and I'll iterate.
