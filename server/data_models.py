from dataclasses import dataclass, asdict
import json

@dataclass
class Article():
    title: str
    publishing_date: str
    summary: str
    url: str

# todo: include historical prices
@dataclass
class StockData():
    valuation_metrics: dict
    profitability_metrics: dict
    balance_sheet_data: dict
    growth_metrics: dict
    stock_performance_metrics: dict
    income_metrics: dict
    analyst_sentiment: dict
    article_sentiments: list[dict]

    def jsonify(self):
        return json.dumps(asdict(self))