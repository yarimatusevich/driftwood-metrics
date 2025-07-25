from transformers import pipeline
from data_models import Article, ArticleSentiment, StockSnapshot

class Finbert():
    def __init__(self):
        self.model = pipeline(model="ProsusAI/finbert")

    def invoke(self, snapshot: StockSnapshot,) -> list[ArticleSentiment]:
        sentiments = []
        articles = snapshot.sentiment.raw_articles

        # Pre-processing the data
        input_texts = [
            "  ".join(filter(None, [article.title, article.summary])) for article in articles
        ]

        responses = self.model(input_texts)

        # Extracting label and score for each article
        sentiments = [
            ArticleSentiment(label=r["label"], score=r["score"]) for r in responses
        ]
        
        # Creating an updated copy of the input snapshot with updated article sentiment 
        updated_snapshot = snapshot.model_copy(
            update={
                "sentiment": snapshot.sentiment.model_copy(
                    update={"news_sentiment": sentiments}
                )
            }
        )

        return updated_snapshot 
        
    def get_sentiment(self, article: Article) -> ArticleSentiment:
        input_text = "  ".join(filter(None, [article.title, article.summary]))

        response = self.model(input_text)
        sentiment = ArticleSentiment(
            label=response[0]["label"],
            score=response[0]["score"]
        )

        return sentiment