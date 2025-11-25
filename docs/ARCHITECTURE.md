# Architecture Documentation

This document provides detailed technical information about The AI Analyst's architecture, design decisions, and implementation details.

## System Overview

The AI Analyst follows a **three-tier architecture**:

```
┌──────────────────────────────────────────────────────────────────┐
│                      PRESENTATION TIER                            │
│                        (Frontend)                                 │
│                                                                   │
│   Next.js 16 + React 19 + Tailwind CSS                          │
│   - Server-side rendering                                        │
│   - Client-side interactivity                                    │
│   - Responsive design                                            │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      APPLICATION TIER                             │
│                        (Backend)                                  │
│                                                                   │
│   FastAPI + Uvicorn                                              │
│   - RESTful API endpoints                                        │
│   - Request validation (Pydantic)                                │
│   - CORS middleware                                              │
│   - Error handling                                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│   Yahoo Finance  │ │  DuckDuckGo  │ │   Anthropic API  │
│    (yfinance)    │ │    (ddgs)    │ │  (Claude 4.5)    │
│                  │ │              │ │                  │
│  • Stock prices  │ │  • News      │ │  • AI analysis   │
│  • Market data   │ │  • Headlines │ │  • Risk rating   │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

## Component Details

### Frontend Architecture

```
frontend/
├── src/app/
│   ├── page.js         # Main dashboard (client component)
│   ├── layout.tsx      # Root layout (server component)
│   └── globals.css     # Global styles
├── public/             # Static assets
└── package.json        # Dependencies
```

#### Key Design Decisions

1. **Client Component for Dashboard** (`"use client"`)
   - Enables useState, useEffect hooks
   - Handles user input and API calls
   - Manages loading/error states

2. **Server Component for Layout**
   - Metadata for SEO
   - Font optimization (Geist fonts)
   - Shared layout structure

3. **Tailwind CSS 4**
   - Utility-first styling
   - No custom CSS files needed
   - Responsive by default

#### State Management

```javascript
const [ticker, setTicker] = useState('');     // User input
const [loading, setLoading] = useState(false); // API call status
const [data, setData] = useState(null);        // API response
const [error, setError] = useState('');        // Error messages
```

### Backend Architecture

```
backend/
├── main.py             # FastAPI application
├── claude_brain.py     # AI analysis logic
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

#### main.py - API Layer

```python
# Responsibilities:
# 1. Initialize FastAPI app
# 2. Configure CORS middleware
# 3. Define API endpoints
# 4. Handle HTTP requests/responses
# 5. Error handling with HTTPException
```

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/analyze/{ticker}` | Stock risk analysis |

#### claude_brain.py - Business Logic

```python
class ClaudeAnalyst:
    def __init__(self):
        # Load API key from environment
        # Initialize Anthropic client
        # Set model configuration

    def fetch_data(self, ticker: str) -> dict:
        # 1. Fetch stock price from Yahoo Finance
        # 2. Fetch news from DuckDuckGo
        # 3. Return structured data

    def analyze(self, ticker: str) -> str:
        # 1. Call fetch_data()
        # 2. Construct prompt with real data
        # 3. Send to Claude API
        # 4. Return analysis text
```

## Data Flow

### Request Flow

```
1. User enters "NVDA" in frontend
                │
                ▼
2. Frontend sends GET /api/analyze/NVDA
                │
                ▼
3. FastAPI receives request
                │
                ▼
4. ClaudeAnalyst.analyze("NVDA") called
                │
                ├──► fetch_data("NVDA")
                │         │
                │         ├──► yfinance: Get price ($177.82)
                │         │
                │         └──► ddgs: Get news headlines
                │
                ▼
5. Construct prompt with real data
                │
                ▼
6. Send to Claude API (Sonnet 4.5)
                │
                ▼
7. Claude returns risk assessment
                │
                ▼
8. FastAPI returns JSON response
                │
                ▼
9. Frontend displays formatted memo
```

### Prompt Engineering

The system uses a carefully crafted prompt structure:

```python
# System Prompt (Persona)
system_prompt = """
You are a cynical, risk-focused hedge fund analyst.
Your job is to protect capital by identifying DOWNSIDE risks.
You do not cheerlead.
"""

# User Prompt (Context + Task)
user_message = f"""
Analyze the stock ticker: {ticker}

HERE IS THE REAL-TIME DATA (Do not hallucinate numbers):
- Current Price: ${price}
- Recent News Headlines:
{news}

TASK:
Write a 'Risk Assessment Memo' (max 150 words).
1. Acknowledge the price action.
2. Identify 2 major risks based on the news provided.
3. Conclude with a 'Bearish' or 'Neutral' rating.
"""
```

**Key Prompt Design Choices:**

| Choice | Reason |
|--------|--------|
| "Cynical" persona | Prevents bullish bias |
| "Do not hallucinate" | Grounds response in provided data |
| Max 150 words | Concise, actionable output |
| Bearish/Neutral only | No bullish option reinforces risk focus |
| Temperature 0.2 | More consistent, factual responses |

## API Configuration

### Claude API Settings

```python
message = self.client.messages.create(
    model="claude-sonnet-4-5-20250929",  # Latest Sonnet
    max_tokens=400,                       # Response length limit
    temperature=0.2,                      # Low = more deterministic
    system=system_prompt,                 # Persona
    messages=[{"role": "user", "content": user_message}]
)
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

### Backend Errors

```python
# API key missing
if not api_key:
    raise ValueError("MISSING API KEY!")

# Analysis endpoint
try:
    report = analyst.analyze(ticker)
    return {"ticker": ticker, "analysis": report}
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Errors

```javascript
try {
    const response = await fetch(`http://127.0.0.1:8000/api/analyze/${ticker}`);
    if (!response.ok) throw new Error("Failed to fetch data");
    const result = await response.json();
    setData(result);
} catch (err) {
    setError("Backend is offline or ticker invalid.");
}
```

## Security Considerations

1. **API Key Protection**
   - Stored in `.env` (not committed)
   - Listed in `.gitignore`
   - Loaded via `python-dotenv`

2. **Input Validation**
   - Ticker converted to uppercase
   - Pydantic models for request validation

3. **CORS**
   - Currently permissive (`*`)
   - Should restrict to specific origins in production

## Performance Considerations

1. **Yahoo Finance**
   - Uses `fast_info` for quicker price retrieval
   - No API key = no rate limit concerns

2. **DuckDuckGo**
   - Limited to 3 results (`max_results=3`)
   - Targeted search query for relevant news

3. **Claude API**
   - `max_tokens=400` limits response size
   - Low temperature reduces retry needs

## Future Improvements

1. **Caching**
   - Cache stock prices (1-5 min TTL)
   - Cache news results (15-30 min TTL)

2. **Async Operations**
   - Make `fetch_data` async
   - Parallel data fetching

3. **Database**
   - Store analysis history
   - User accounts and watchlists

4. **Authentication**
   - JWT-based auth
   - Rate limiting per user

5. **Additional Data Sources**
   - SEC filings
   - Earnings data
   - Technical indicators
