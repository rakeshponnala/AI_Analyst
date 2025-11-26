# HedgeAI API Documentation

Complete API reference for the HedgeAI backend service.

## Base URL

```
http://127.0.0.1:8000
```

**Production:** `https://your-domain.com`

## API Version

Current version: **v1**

All endpoints are prefixed with `/v1/`

## Authentication

Currently, no authentication is required for API endpoints. **Rate limiting is enforced.**

## Rate Limiting

- **Limit:** 10 requests per minute per IP address
- **Response:** `429 Too Many Requests` when limit exceeded

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /v1/`

**Response:**
```json
{
  "status": "active",
  "message": "HedgeAI API is online",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Analyze Stock

Get comprehensive risk analysis for a stock.

**Endpoint:** `GET /v1/api/analyze/{query}`

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| query | string | path | Yes | Stock ticker (e.g., "NVDA") or company name (e.g., "google") |

**Example Requests:**

```bash
# Using ticker
curl http://127.0.0.1:8000/v1/api/analyze/NVDA

# Using company name
curl http://127.0.0.1:8000/v1/api/analyze/google
```

**Success Response (200 OK):**

```json
{
  "ticker": "NVDA",
  "company_name": "NVIDIA Corporation",
  "rating": "BEARISH",
  "metrics": {
    "price": 135.58,
    "price_change": -2.35,
    "price_change_pct": -1.70,
    "prev_close": 137.93,
    "week_52_high": 152.89,
    "week_52_low": 39.23,
    "pct_from_high": -11.3,
    "market_cap": "$3.33T",
    "pe_ratio": 57.34,
    "forward_pe": 28.45,
    "volume_vs_avg": 105,
    "beta": 1.73,
    "short_percent": 1.24,
    "debt_to_equity": 14.23,
    "current_ratio": 3.89,
    "profit_margin": 55.04,
    "revenue_growth": 122.40,
    "earnings_growth": 168.00,
    "target_price": 150.00,
    "target_upside": 10.6,
    "recommendation": "buy"
  },
  "news": [
    {
      "title": "NVIDIA Announces Q4 Results",
      "source": "Reuters",
      "url": "https://example.com/news/1"
    }
  ],
  "analysis": "**RISK ASSESSMENT: NVDA**\n\nNVIDIA trades at $135.58...",
  "generated_at": "2025-11-26 12:00:00"
}
```

**Error Responses:**

**400 Bad Request - Invalid Ticker:**
```json
{
  "detail": "Invalid ticker symbol or company name"
}
```

**400 Bad Request - Invalid Format:**
```json
{
  "detail": "Invalid ticker format. Only letters, numbers, dots and hyphens allowed."
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An unexpected error occurred during analysis"
}
```

**503 Service Unavailable:**
```json
{
  "detail": "Analysis service unavailable. Check API key configuration."
}
```

## Data Models

### StockMetrics

| Field | Type | Description |
|-------|------|-------------|
| price | number/string | Current stock price |
| price_change | number/string | Daily price change in dollars |
| price_change_pct | number/string | Daily price change percentage |
| prev_close | number/string | Previous closing price |
| week_52_high | number/string | 52-week high price |
| week_52_low | number/string | 52-week low price |
| pct_from_high | number/string | Percentage from 52-week high |
| market_cap | string | Market capitalization (formatted) |
| pe_ratio | number/string | Trailing P/E ratio |
| forward_pe | number/string | Forward P/E ratio |
| volume_vs_avg | number/string | Volume vs average (%) |
| beta | number/string | Stock beta (volatility vs market) |
| short_percent | number/string | Short interest percentage |
| debt_to_equity | number/string | Debt-to-equity ratio |
| current_ratio | number/string | Current ratio (liquidity) |
| profit_margin | number/string | Net profit margin (%) |
| revenue_growth | number/string | YoY revenue growth (%) |
| earnings_growth | number/string | YoY earnings growth (%) |
| target_price | number/string | Analyst target price |
| target_upside | number/string | Upside to target (%) |
| recommendation | string | Analyst recommendation |

**Note:** Fields may contain "N/A" when data is unavailable.

### NewsItem

| Field | Type | Description |
|-------|------|-------------|
| title | string | News headline |
| source | string | News source |
| url | string (optional) | Link to article |

## Response Formats

All responses use `application/json` content type.

## Error Handling

The API uses standard HTTP status codes:

- **2xx** - Success
- **4xx** - Client errors (bad request, validation, rate limit)
- **5xx** - Server errors

Error responses include a `detail` field with human-readable message.

## Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1732627200
```

## Best Practices

1. **Handle rate limits gracefully** - Implement backoff/retry logic
2. **Cache responses** - Stock data changes infrequently
3. **Validate input** - Check ticker format before sending
4. **Handle "N/A" values** - Many metrics may be unavailable
5. **Use timeouts** - Set reasonable timeout values (30-60s)

## Examples

### Python

```python
import requests

response = requests.get("http://127.0.0.1:8000/v1/api/analyze/AAPL")
if response.status_code == 200:
    data = response.json()
    print(f"Ticker: {data['ticker']}")
    print(f"Rating: {data['rating']}")
    print(f"Analysis: {data['analysis'][:200]}...")
elif response.status_code == 429:
    print("Rate limit exceeded")
else:
    print(f"Error: {response.json()['detail']}")
```

### JavaScript

```javascript
const response = await fetch('http://127.0.0.1:8000/v1/api/analyze/TSLA');
if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`);
}
const data = await response.json();
console.log(data.ticker, data.rating);
```

### curl

```bash
# Basic request
curl http://127.0.0.1:8000/v1/api/analyze/MSFT

# With pretty printing
curl http://127.0.0.1:8000/v1/api/analyze/MSFT | jq .

# Save to file
curl http://127.0.0.1:8000/v1/api/analyze/GOOGL -o analysis.json
```

## Support

For issues or questions:
- GitHub Issues: [Report bugs](https://github.com/yourrepo/issues)
- Documentation: See README.md

---

**Version:** 1.0.0
**Last Updated:** 2025-11-26
