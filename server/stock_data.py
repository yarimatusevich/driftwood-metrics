import yfinance
import json

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

def get_data_from_ticker(ticker: str):
    return yfinance.Ticker(ticker)

def parse_data(data: dict):
    data = data.news
    
    parsed_data = []
    # print(data[0])

    for article in data:
        article_content = article.get("content")

        title = article_content.get("title")
        publishing_date = article_content.get("pubDate")
        thumbnail = article_content.get("thumbnail")
        summary = article_content.get("summary")
        url = article_content.get("clickThroughUrl").get("url")

        new_article = Article(title, publishing_date, thumbnail, summary, url)
        parsed_data.append(new_article)
    
    return parsed_data

data = get_data_from_ticker("AMZN")
articles = parse_data(data)
print(articles[0])