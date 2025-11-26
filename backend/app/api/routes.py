from fastapi import APIRouter, HTTPException, Request
import re

from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.schemas import AnalysisResponse, HealthResponse, StockMetrics, NewsItem
from app.services.analysis_service import AnalysisService
from app.services.ticker_service import TickerService
from app.middleware.rate_limiter import limiter

logger = get_logger(__name__)

router = APIRouter()

# Initialize services
try:
    analysis_service = AnalysisService()
    ticker_service = TickerService()
    logger.info("[API] Analysis service loaded successfully")
except Exception as e:
    logger.error(f"[API] Failed to initialize analysis service: {e}")
    analysis_service = None
    ticker_service = TickerService()


@router.get("/v1/", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns the current status of the API.
    """
    return HealthResponse(
        status="active",
        message="HedgeAI API is online",
        version=settings.API_VERSION
    )


@router.get(
    "/v1/api/analyze/{query}",
    response_model=AnalysisResponse,
    tags=["Analysis"]
)
@limiter.limit("10/minute")
async def analyze_stock(request: Request, query: str):
    """
    Analyze a stock for investment risks.

    Args:
        request: FastAPI request object (for rate limiting)
        query: Stock ticker symbol OR company name (e.g., NVDA, TSLA, AAPL, "google", "apple")

    Returns:
        Structured analysis with metrics, news, and AI assessment
    """
    if not analysis_service:
        raise HTTPException(
            status_code=503,
            detail="Analysis service unavailable. Check API key configuration."
        )

    # Resolve company name to ticker if needed
    ticker = ticker_service.resolve_ticker(query)

    # Validate ticker format
    if not ticker or len(ticker) > 10:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticker symbol or company name"
        )

    # Sanitize ticker - only allow alphanumeric, hyphens, and dots
    if not re.match(r'^[A-Z0-9.\-]+$', ticker):
        raise HTTPException(
            status_code=400,
            detail="Invalid ticker format. Only letters, numbers, dots and hyphens allowed."
        )

    logger.info(f"[API] ========== NEW ANALYSIS REQUEST ==========")
    logger.info(f"[API] Original query: '{query}'")
    logger.info(f"[API] Resolved ticker: '{ticker}'")

    try:
        result = await analysis_service.analyze(ticker)
        logger.info(f"[API] Analysis completed successfully for {ticker}")
        logger.info(f"[API] Price returned: {result['metrics']['price']}")

        # Build structured response
        return AnalysisResponse(
            ticker=result["ticker"],
            company_name=result["company_name"],
            rating=result["rating"],
            metrics=StockMetrics(
                price=result["metrics"]["price"],
                price_change=result["metrics"]["price_change"],
                price_change_pct=result["metrics"]["price_change_pct"],
                prev_close=result["metrics"]["prev_close"],
                week_52_high=result["metrics"]["week_52_high"],
                week_52_low=result["metrics"]["week_52_low"],
                pct_from_high=result["metrics"]["pct_from_high"],
                market_cap=result["metrics"]["market_cap"],
                pe_ratio=result["metrics"]["pe_ratio"],
                forward_pe=result["metrics"]["forward_pe"],
                volume_vs_avg=result["metrics"]["volume_vs_avg"],
                beta=result["metrics"]["beta"],
                short_percent=result["metrics"]["short_percent"],
                debt_to_equity=result["metrics"]["debt_to_equity"],
                current_ratio=result["metrics"]["current_ratio"],
                profit_margin=result["metrics"]["profit_margin"],
                revenue_growth=result["metrics"]["revenue_growth"],
                earnings_growth=result["metrics"]["earnings_growth"],
                target_price=result["metrics"]["target_price"],
                target_upside=result["metrics"]["target_upside"],
                recommendation=result["metrics"]["recommendation"]
            ),
            news=[
                NewsItem(
                    title=item["title"],
                    source=item["source"],
                    url=item.get("url")
                ) for item in result["news"]
            ],
            analysis=result["analysis"],
            generated_at=result["generated_at"]
        )

    except RuntimeError as e:
        logger.error(f"[API] RuntimeError: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"[API] Unexpected error: {e}")
        logger.exception("[API] Full traceback:")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis"
        )
