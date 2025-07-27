from data_models import Article, ArticleSentiment, StockSnapshot
from transformers import pipeline

class Finbert():
    def __init__(self):
        self.model = pipeline(model="ProsusAI/finbert")

    def invoke(self, snapshot: StockSnapshot,) -> StockSnapshot:
        articles = snapshot.sentiment.articles

        # Pre-processing the data
        input_texts = [
            "  ".join(filter(None, [article.title, article.summary])) for article in articles
        ]

        responses = self.model(input_texts)

        # Updating articles
        for article, response in zip(articles, responses):
            article.sentiment = ArticleSentiment(label=response["label"], score=response["score"])
            
        return snapshot 
        
    def get_sentiment(self, article: Article) -> ArticleSentiment:
        input_text = "  ".join(filter(None, [article.title, article.summary]))

        response = self.model(input_text)
        sentiment = ArticleSentiment(
            label=response[0]["label"],
            score=response[0]["score"]
        )

        return sentiment