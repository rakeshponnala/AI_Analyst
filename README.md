# HedgeAI

AI-powered contrarian stock risk analysis for retail investors. Unlike traditional bullish-biased tools, HedgeAI takes a **hedge fund approach** - identifying downside risks to help protect your capital.

## Overview

Most financial analysis tools default to optimism. HedgeAI fills a critical gap by providing **"Devil's Advocate"** analysis that surfaces potential risks before you invest.

**Key Value Proposition:**
- Identifies risks others might overlook
- Provides clear, actionable risk assessments
- Helps investors make more informed decisions

## Features

| Feature | Description |
|---------|-------------|
| **Real-time Data** | Live stock prices via Yahoo Finance |
| **News Intelligence** | Recent headlines aggregated from DuckDuckGo |
| **AI Risk Analysis** | Claude Sonnet 4.5 powered risk assessment |
| **Clear Verdicts** | Bearish or Neutral ratings |
| **Modern UI** | Clean, responsive dashboard |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│                                                              │
│    Next.js 16  •  React 19  •  Tailwind CSS 4              │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│                                                              │
│    FastAPI  •  Pydantic  •  Uvicorn                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Yahoo     │  │ DuckDuckGo │  │ Anthropic  │
    │  Finance   │  │   Search   │  │  Claude    │
    └────────────┘  └────────────┘  └────────────┘
```

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend | Next.js | 16.x |
| UI Framework | React | 19.x |
| Styling | Tailwind CSS | 4.x |
| Backend | FastAPI | Latest |
| AI Model | Claude Sonnet | 4.5 |
| Stock Data | yfinance | Latest |
| News Data | ddgs | Latest |

## Project Structure

```
HedgeAI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py             # API endpoint definitions
│   │   ├── core/
│   │   │   └── config.py             # Application configuration
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic data models
│   │   └── services/
│   │       ├── analysis_service.py   # AI analysis logic
│   │       └── data_service.py       # Data retrieval logic
│   ├── main.py                       # Application entry point
│   ├── requirements.txt              # Python dependencies
│   └── .env                          # Environment variables (not committed)
│
├── frontend/
│   ├── src/app/
│   │   ├── page.js                   # Main dashboard
│   │   ├── layout.tsx                # Root layout
│   │   └── globals.css               # Global styles
│   └── package.json                  # Node dependencies
│
├── docs/
│   └── ARCHITECTURE.md               # Technical documentation
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **Anthropic API key** → [Get one here](https://console.anthropic.com/)
- **Docker** (optional) → [Get Docker](https://www.docker.com/get-started)

### Quick Start with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/HedgeAI.git
cd HedgeAI

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# Build and run with Docker Compose
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Then edit with your API key
```

**Environment Variables** (`backend/.env`):
```env
# Required
ANTHROPIC_API_KEY=your_api_key_here

# AI Configuration
AI_MODEL_NAME=claude-sonnet-4-5-20250929
AI_MAX_TOKENS=1500
AI_TEMPERATURE=0.3
NEWS_MAX_RESULTS=5

# API Timeouts (seconds)
EXTERNAL_API_TIMEOUT=30
ANTHROPIC_API_TIMEOUT=60

# Cache TTL (seconds)
STOCK_DATA_CACHE_TTL=300
NEWS_CACHE_TTL=900

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Start the server:**
```bash
uvicorn main:app --reload
```

API available at `http://127.0.0.1:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.local.example .env.local
# Edit if you need to change the backend URL

# Start development server
npm run dev
```

**Environment Variables** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Dashboard available at `http://localhost:3000`

## API Documentation

### Interactive Docs

Once the backend is running:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### API Reference

**Full API documentation:** [`backend/API.md`](backend/API.md)

#### Rate Limiting

- **10 requests per minute** per IP address
- Exceeding limit returns `429 Too Many Requests`

#### Endpoints

##### Health Check
```http
GET /v1/
```
**Response:**
```json
{
  "status": "active",
  "message": "HedgeAI API is online",
  "version": "1.0.0"
}
```

##### Analyze Stock
```http
GET /v1/api/analyze/{query}
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `query` | string | Stock ticker (e.g., NVDA) or company name (e.g., "google") |

**Example Response:**
```json
{
  "ticker": "NVDA",
  "company_name": "NVIDIA Corporation",
  "rating": "BEARISH",
  "metrics": {
    "price": 135.58,
    "pe_ratio": 57.34,
    "beta": 1.73,
    ...
  },
  "news": [...],
  "analysis": "**RISK ASSESSMENT: NVDA**\n\nNVIDIA trades at $135.58...",
  "generated_at": "2025-11-26 12:00:00"
}
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint
flake8 app/ tests/ --max-line-length=100

# Type check
mypy app/ --ignore-missing-imports
```

### Pre-commit Hooks

```bash
# Install
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

## Development

### Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### CI/CD

GitHub Actions runs automatically on:
- Push to `main` or `develop`
- Pull requests

Checks include:
- Backend tests with pytest
- Frontend build verification
- Code linting (Black, flake8, ESLint)
- Docker build tests

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for details.

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Required |
| `AI_MODEL_NAME` | Claude model ID | `claude-sonnet-4-5-20250929` |
| `AI_MAX_TOKENS` | Max response tokens | `400` |
| `AI_TEMPERATURE` | Response randomness | `0.2` |
| `NEWS_MAX_RESULTS` | Headlines to fetch | `3` |

## Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - Technical deep-dive into system design
- **[API Reference](backend/API.md)** - Complete API documentation
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project

## Roadmap

- [ ] User authentication
- [ ] Analysis history
- [ ] Portfolio tracking
- [ ] Additional data sources (SEC filings, earnings)
- [ ] Technical indicators

## Limitations

- Stock prices may have slight delays
- News availability depends on DuckDuckGo
- Analysis is AI-generated and for research only

## Disclaimer

**This tool is for educational and research purposes only.**

HedgeAI does not provide financial advice. Always conduct your own research and consult qualified financial advisors before making investment decisions. Past performance does not guarantee future results.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read our **[Contributing Guide](CONTRIBUTING.md)** for:
- Development setup instructions
- Code style guidelines
- Testing requirements
- Pull request process

---

Built by Rakesh Ponnala
