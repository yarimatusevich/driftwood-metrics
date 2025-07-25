from data_models import (
    Article,
    CompanyProfile,
    StockSnapshot,
    ValuationMetrics,
    ProfitabilityMetrics,
    BalanceSheetMetrics,
    GrowthMetrics,
    PerformanceMetrics,
    IncomeMetrics,
    FinancialMetrics,
    HistoricalPrice,
    MarketData,
    SentimentData,
)
from sentiment import Finbert
import yfinance
from yfinance import Ticker

def create_ticker_object(ticker_symbol: str) -> Ticker:
    try:
        return yfinance.Ticker(ticker_symbol)
    except Exception as e :
        print(f"Error retrieving ticker: {e}")
        return None

def create_stock_snapshot(ticker_symbol: Ticker) -> StockSnapshot:
    ticker = create_ticker_object(ticker_symbol)

    return StockSnapshot(
        profile=get_company_profile(ticker),
        financials=get_financial_metrics(ticker),
        market_data=get_market_data(ticker),
        sentiment=get_sentiment_data(ticker)
    )

def get_company_profile(ticker: Ticker) -> CompanyProfile:
    return CompanyProfile(
        name=ticker.info.get("longName") or ticker.info.get("shortName"),
        ticker=ticker.info.get("symbol"),
        industry=ticker.info.get("industry"),
        sector= ticker.info.get("sector"),
        summary=ticker.info.get("longBusinessSummary")
    )

def get_financial_metrics(ticker: Ticker) -> FinancialMetrics:
    return FinancialMetrics(
        valuation=get_valuation_metrics(ticker),
        profitability=get_profitabilty_metrics(ticker),
        balance_sheet=get_balance_sheet_metrics(ticker),
        growth=get_growth_metrics(ticker),
        performance=get_performance_metrics(ticker),
        income=get_income_metrics(ticker)
    )

def get_valuation_metrics(ticker: Ticker) -> ValuationMetrics:
    return ValuationMetrics(
        trailing_pe=ticker.info.get("trailingPE"),
        forward_pe=ticker.info.get("forwardPE"),
        market_cap=ticker.info.get("marketCap")
    )

def get_profitabilty_metrics(ticker: Ticker) -> ProfitabilityMetrics:
    return ProfitabilityMetrics(
        profit_margins=ticker.info.get("profitMargins"),
        return_on_equity=ticker.info.get("returnOnEquity")
    )

def get_balance_sheet_metrics(ticker: Ticker) -> BalanceSheetMetrics:
    return BalanceSheetMetrics(
        total_cash=ticker.info.get("totalCash"),
        total_debt=ticker.info.get("totalDebt")
    )

def get_growth_metrics(ticker: Ticker) -> GrowthMetrics:
    return GrowthMetrics(
        revenue_growth=ticker.info.get("revenueGrowth"),
        earnings_growth=ticker.info.get("earningsGrowth")
    )

def get_performance_metrics(ticker: Ticker) -> PerformanceMetrics:
    return PerformanceMetrics(
        beta=ticker.info.get("beta"),
        eps_trailing=ticker.info.get("trailingEps")
    )

def get_income_metrics(ticker: Ticker) -> IncomeMetrics:
    return IncomeMetrics(
        total_revenue = ticker.info.get("totalRevenue"),
        net_income = ticker.info.get("netIncomeToCommon")
    )

def get_market_data(ticker: Ticker) -> MarketData:
    return MarketData(
        historical_prices=get_weekly_historical_prices(ticker)
    )

def get_weekly_historical_prices(ticker: Ticker) -> list[HistoricalPrice]:
    hist = ticker.history(period='6mo', interval='1wk')

    weekly_prices = []

    for _, row in hist.iterrows():
        hp = HistoricalPrice(
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=int(row['Volume'])
        )
        weekly_prices.append(hp)
    
    return weekly_prices

def get_sentiment_data(ticker: Ticker) -> SentimentData:
    return SentimentData(
        analyst_summary=ticker.info.get("averageAnalystRating"),
        news_sentiment=None,
        raw_articles=get_news_articles(ticker)
    )

def get_news_articles(ticker: Ticker) -> list[Article]:
    data = ticker.news
    articles = []

    for article in data:
        article_content = article.get("content")
        title = article_content.get("title")
        publishing_date = article_content.get("pubDate")
        summary = article_content.get("summary")

        clickthrough = article_content.get("clickThroughUrl")
        url = clickthrough.get("url") if isinstance(clickthrough, dict) else None

        article = Article(title=title, publishing_date=publishing_date, summary=summary, url=url)
        articles.append(article)
    
    return articles