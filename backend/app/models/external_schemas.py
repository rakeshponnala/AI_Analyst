"""Pydantic schemas for validating external API responses."""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class YahooFinanceInfo(BaseModel):
    """Schema for Yahoo Finance info data."""

    shortName: Optional[str] = None
    previousClose: Optional[float] = None
    fiftyTwoWeekHigh: Optional[float] = None
    fiftyTwoWeekLow: Optional[float] = None
    marketCap: Optional[int] = None
    trailingPE: Optional[float] = None
    forwardPE: Optional[float] = None
    averageVolume: Optional[int] = None
    beta: Optional[float] = None
    shortPercentOfFloat: Optional[float] = None
    debtToEquity: Optional[float] = None
    profitMargins: Optional[float] = None
    revenueGrowth: Optional[float] = None
    earningsGrowth: Optional[float] = None
    currentRatio: Optional[float] = None
    targetMeanPrice: Optional[float] = None
    targetMedianPrice: Optional[float] = None
    targetHighPrice: Optional[float] = None
    targetLowPrice: Optional[float] = None
    numberOfAnalystOpinions: Optional[int] = None
    recommendationKey: Optional[str] = None

    class Config:
        extra = "allow"  # Allow additional fields from Yahoo Finance

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_string(cls, v):
        """Convert 'N/A' strings to None."""
        if v == "N/A" or v == "":
            return None
        return v


class YahooFinanceFastInfo(BaseModel):
    """Schema for Yahoo Finance fast_info data."""

    last_price: float
    last_volume: int
