import yfinance

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
    try:
        return yfinance.Ticker(ticker)
    
    except Exception as e :
        print(f"Error retrieving ticker: {e}")
        return None

def parse_data(data: dict):
    # Checking if data is not null
    if not isinstance(data, dict):
        return

    data = data.news
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