# The AI Analyst

A specialized AI-powered tool for retail investors that provides **"Devil's Advocate"** risk analysis on stocks. Instead of cheerleading, it identifies downside risks and provides bearish/neutral ratings to help protect capital.

## Why This Exists

Most financial tools and analysts are bullish by default. The AI Analyst takes the opposite approach - it acts as a **cynical hedge fund analyst** focused on identifying risks that could hurt your investment. This helps retail investors make more informed decisions by understanding the bear case.

## Features

- **Real-time Stock Data** - Fetches live prices via Yahoo Finance
- **News Aggregation** - Pulls recent headlines via DuckDuckGo search
- **AI Risk Assessment** - Claude Sonnet 4.5 analyzes data and identifies key risks
- **Bearish/Neutral Ratings** - Clear verdict on risk level
- **Clean Dashboard UI** - Modern React frontend with Tailwind CSS

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                   │
│                     Enter ticker: "NVDA"                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                              │
│                                                                      │
│  • React dashboard with search input                                │
│  • Sends GET request to /api/analyze/{ticker}                       │
│  • Displays formatted risk memo                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                               │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   DATA RETRIEVAL LAYER                       │   │
│  │                                                               │   │
│  │   Yahoo Finance (yfinance)     DuckDuckGo (ddgs)            │   │
│  │   ─────────────────────────    ─────────────────            │   │
│  │   • Current stock price        • Recent news headlines       │   │
│  │   • Fast, no API key needed    • Risk-focused search query   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   AI ANALYSIS LAYER                          │   │
│  │                                                               │   │
│  │   Claude Sonnet 4.5 (Anthropic API)                         │   │
│  │   ─────────────────────────────────                         │   │
│  │   System Prompt: "Cynical hedge fund analyst"                │   │
│  │   • Analyzes price + news                                    │   │
│  │   • Identifies 2 major risks                                 │   │
│  │   • Returns Bearish/Neutral rating                           │   │
│  │   • Low temperature (0.2) for consistency                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT                                       │
│                                                                      │
│   RISK ASSESSMENT MEMO - NVDA                                       │
│   ─────────────────────────────                                     │
│   Price: $177.82                                                    │
│                                                                      │
│   Major Risks:                                                       │
│   1. Taiwan/TSMC geopolitical exposure...                           │
│   2. Valuation concerns from analysts...                            │
│                                                                      │
│   Rating: BEARISH                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 16 + React 19 | Dashboard UI |
| **Styling** | Tailwind CSS 4 | Modern, responsive design |
| **Backend** | FastAPI (Python) | REST API server |
| **AI Model** | Claude Sonnet 4.5 | Risk analysis generation |
| **Stock Data** | yfinance | Real-time price data |
| **News Data** | DuckDuckGo Search | Recent headlines |

## Project Structure

```
AI_Analyst/
├── backend/
│   ├── main.py              # FastAPI server & endpoints
│   ├── claude_brain.py      # AI analysis logic
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API keys (not committed)
│
├── frontend/
│   ├── src/app/
│   │   ├── page.js          # Main dashboard component
│   │   ├── layout.tsx       # App layout & metadata
│   │   └── globals.css      # Tailwind styles
│   ├── package.json         # Node dependencies
│   └── ...
│
├── docs/
│   └── ARCHITECTURE.md      # Technical documentation
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=your_api_key_here
AI_MODEL_NAME=claude-sonnet-4-5-20250929
```

Start the server:
```bash
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`

## API Reference

### Health Check
```
GET /
```
Response:
```json
{"status": "active", "message": "The AI Analyst Brain is Online"}
```

### Analyze Stock
```
GET /api/analyze/{ticker}
```
Parameters:
- `ticker` (string): Stock symbol (e.g., NVDA, TSLA, AAPL)

Response:
```json
{
  "ticker": "NVDA",
  "analysis": "RISK ASSESSMENT MEMO - NVDA\n\nPrice: $177.82\n\nMajor Risks:\n1. Taiwan/TSMC geopolitical exposure...\n2. Valuation concerns...\n\nRating: BEARISH"
}
```

## Example Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Enter a stock ticker (e.g., `NVDA`, `TSLA`, `AAPL`)
4. Click "Run Analysis" or press Enter
5. Review the AI-generated risk assessment

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `AI_MODEL_NAME` | Claude model to use | `claude-sonnet-4-5-20250929` |

## Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - Detailed technical documentation

## Limitations

- News data depends on DuckDuckGo search availability
- Stock prices may have slight delays (not real-time trading data)
- AI analysis is for research purposes only

## Disclaimer

**This tool is for educational and research purposes only. It is NOT financial advice.** Always do your own research and consult with qualified financial advisors before making investment decisions.

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a PR.
