import yfinance
from yfinance import Ticker
from data_models import StockData, Article
from sentiment_model import get_sentiment_model, get_article_list_sentiments

def create_ticker_object(ticker: str) -> Ticker:
    try:
        return yfinance.Ticker(ticker)
    
    except Exception as e :
        print(f"Error retrieving ticker: {e}")
        return None

def parse_ticker_data(ticker: Ticker) -> StockData:
    model = get_sentiment_model()
    articles = get_news_articles(ticker)
    
    return StockData(
        valuation_metrics = get_valuation_metrics(ticker),
        profitability_metrics = get_profitability_metrics(ticker),
        balance_sheet_data = get_balance_sheet_data(ticker),
        growth_metrics = get_growth_metrics(ticker),
        stock_performance_metrics = get_stock_performance_metrics(ticker),
        income_metrics = get_income_metrics(ticker),
        analyst_sentiment = get_analyst_sentiment(ticker),
        article_sentiments = get_article_list_sentiments(articles, model)
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
        "recommendations": ticker.recommendations.to_dict(orient = "records"),
    }

def get_news_articles(ticker: Ticker) -> list[Article]:
    data = ticker.news
    parsed_data = []

    for i, article in enumerate(data):
        try:
            article_content = article.get("content")
            title = article_content.get("title")
            publishing_date = article_content.get("pubDate")

            # thumbnail_data = article_content.get("thumbnail")
            # thumbnail = thumbnail_data.get("originalUrl") if isinstance(thumbnail_data, dict) else None

            summary = article_content.get("summary")

            clickthrough = article_content.get("clickThroughUrl")
            url = clickthrough.get("url") if isinstance(clickthrough, dict) else None

            new_article = Article(title, publishing_date, summary, url)
            parsed_data.append(new_article)
        except Exception as e:
            print(f"Error parsing article at index {i}: {e}")
    
    return parsed_data
