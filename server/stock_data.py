import yfinance
from yfinance import Ticker

class Article():
    def __init__(self, title: str, publishing_date: str, thumbnail: str, summary: str, url: str):
        self.title = title
        self.publishing_date = publishing_date
        self.thumbnail = thumbnail
        self.summary = summary
        self.url = url
    
    def __str__(self):
        return f"Title: {self.title}, Publishing Date: {self.publishing_date}, thumbnail: {self.thumbnail}, summary: {self.summary}, url: {self.url} "

    title: str
    publishing_date: str
    summary: str
    url: str

"""
todo: include historical price trends
"""
class StockData():
    def __init__(
        self,
        valuation_metrics: dict,
        profitability_metrics: dict,
        balance_sheet_data: dict,
        growth_metrics: dict,
        stock_performance_metrics: dict,
        income_metrics: dict,
        analyst_sentiment: dict,
        # news_articles: list[Article]
    ):
        self.valuation_metrics = valuation_metrics
        self.profitability_metrics = profitability_metrics
        self.balance_sheet_data = balance_sheet_data
        self.growth_metrics = growth_metrics
        self.stock_performance_metrics = stock_performance_metrics
        self.income_metrics = income_metrics
        self.analyst_sentiment = analyst_sentiment
        # self.news_articles = news_articles

    valuation_metrics: dict
    profitability_metrics: dict
    balance_sheet_data: dict
    growth_metrics: dict
    stock_performance_metrics: dict
    income_metrics: dict
    analyst_sentiment: dict
    # news_articles: list[Article]

"""
Retrieves ticker data from Yahoo Finance and creates a ticker object
"""
def create_ticker_object(ticker: str) -> Ticker:
    try:
        return yfinance.Ticker(ticker)
    
    except Exception as e :
        print(f"Error retrieving ticker: {e}")
        return None

def parse_ticker_data(ticker: Ticker) -> StockData:
    return StockData(
        valuation_metrics = get_valuation_metrics(ticker),
        profitability_metrics = get_profitability_metrics(ticker),
        balance_sheet_data = get_balance_sheet_data(ticker),
        growth_metrics = get_growth_metrics(ticker),
        stock_performance_metrics = get_stock_performance_metrics(ticker),
        income_metrics = get_income_metrics(ticker),
        analyst_sentiment = get_analyst_sentiment(ticker),
        # news_articles = get_news_articles(ticker)
    )

def get_valuation_metrics(ticker: Ticker) -> dict:
    return {
        "trailingPE": ticker.info.get("trailingPE"),
        "forwardPE": ticker.info.get("forwardPE")
    }

def get_profitability_metrics(ticker: Ticker) -> dict:
    return {
        "epsTrailingTwelveMonths": ticker.info.get("epsTrailingTwelveMonths"),
        "totalRevenue": ticker.info.get("totalRevenue"),
        "profitMargins": ticker.info.get("profitMargins"),
        "returnOnEquity": ticker.info.get("returnOnEquity"),
        "operatingMargins": ticker.info.get("operatingMargins")
    }

def get_balance_sheet_data(ticker: Ticker) -> dict:
    return {
        "totalDebt": ticker.info.get("totalDebt"),
        "totalCash": ticker.info.get("totalCash"),
        "currentRatio": ticker.info.get("currentRatio"),
        "debtToEquity": ticker.info.get("debtToEquity"),
    }

def get_growth_metrics(ticker: Ticker) -> dict:
    return {
        "revenueGrowth": ticker.info.get("revenueGrowth"),
        "earningsQuarterlyGrowth": ticker.info.get("earningsQuarterlyGrowth"),
    }

def get_stock_performance_metrics(ticker: Ticker) -> dict:
    return {
        "fiftyTwoWeekLow": ticker.info.get("fiftyTwoWeekLow"),
        "fiftyTwoWeekHigh": ticker.info.get("fiftyTwoWeekHigh"),
        "beta": ticker.info.get("beta"),
    }

def get_income_metrics(ticker: Ticker) -> dict:
    return {
        "dividendYield": ticker.info.get("dividendYield"),
    }

def get_analyst_sentiment(ticker: Ticker) -> dict:
    return {
        "targetMeanPrice": ticker.info.get("targetMeanPrice"),
        "recommendations": ticker.recommendations,
    }

"""
Parses ten most recent articles from ticker object and returns list of article objects
""" 
def get_news_articles(ticker: Ticker) -> list[Article]:
    data = ticker.news
    parsed_data = []

    for i, article in enumerate(data):
        try:
            article_content = article.get("content")
            title = article_content.get("title")
            publishing_date = article_content.get("pubDate")

            thumbnail_data = article_content.get("thumbnail")
            thumbnail = thumbnail_data.get("originalUrl") if isinstance(thumbnail_data, dict) else None

            summary = article_content.get("summary")

            clickthrough = article_content.get("clickThroughUrl")
            url = clickthrough.get("url") if isinstance(clickthrough, dict) else None

            new_article = Article(title, publishing_date, thumbnail, summary, url)
            parsed_data.append(new_article)
        except Exception as e:
            print(f"Error parsing article at index {i}: {e}")
    
    return parsed_data