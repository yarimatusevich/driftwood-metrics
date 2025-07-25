from pydantic import BaseModel

class ValuationMetrics(BaseModel):
    trailing_pe: float | None
    forward_pe: float | None
    market_cap: float | None

class ProfitabilityMetrics(BaseModel):
    profit_margins: float | None
    return_on_equity: float | None

class BalanceSheetMetrics(BaseModel):
    total_cash: float | None
    total_debt: float | None

class GrowthMetrics(BaseModel):
    revenue_growth: float | None
    earnings_growth: float | None

class PerformanceMetrics(BaseModel):
    beta: float | None
    eps_trailing: float | None

class IncomeMetrics(BaseModel):
    total_revenue: float | None
    net_income: float | None

class Article(BaseModel):
    title: str
    publishing_date: str
    summary: str
    url: str | None

class ArticleSentiment(BaseModel):
    label: str
    score: float

class HistoricalPrice(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int

class CompanyProfile(BaseModel):
    name: str
    ticker: str
    industry: str
    sector: str
    summary: str

class FinancialMetrics(BaseModel):
    valuation: ValuationMetrics
    profitability: ProfitabilityMetrics
    balance_sheet: BalanceSheetMetrics
    growth: GrowthMetrics
    performance: PerformanceMetrics
    income: IncomeMetrics

class MarketData(BaseModel):
    historical_prices: list[HistoricalPrice]

class SentimentData(BaseModel):
    analyst_summary: str | None
    news_sentiment: list[ArticleSentiment] | None
    raw_articles: list[Article] | None

class StockSnapshot(BaseModel):
    profile: CompanyProfile
    financials: FinancialMetrics
    market_data: MarketData
    sentiment: SentimentData

class StockAnalysis(BaseModel):
    financials: str
    # market_data_analysis: str
    sentiment: str
    summary: str
    recommendation: str