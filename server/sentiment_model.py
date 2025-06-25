"""
sentiment.py

This module handles article-level sentiment analysis.

It includes functions to:
- Load a sentiment classification model (e.g., via HuggingFace's pipeline)
- Process a list of Article objects
- Generate sentiment labels (e.g., positive/neutral/negative) based on article title and summary

Intended for use in financial analysis workflows where article sentiment is used as a signal for investment decision-making.
"""

from transformers import pipeline, TextClassificationPipeline
from data_models import Article

def get_sentiment_model() -> TextClassificationPipeline:
    model_name = "ProsusAI/finbert"
    return pipeline(model = model_name)

def prompt_sentiment_model(input: str, model: TextClassificationPipeline) -> dict:
    return model(input)

def get_article_list_sentiments(article_list: list[Article], model: TextClassificationPipeline) -> list[dict]:
    sentiments = []

    for article in article_list:
        current_article_sentiment = get_article_sentiment(article, model)
        sentiments.append(current_article_sentiment)
    
    return sentiments

def get_article_sentiment(article: Article, model: TextClassificationPipeline) -> dict:
    # filters out null, joins with space
    input_text = " ".join(filter(None, [article.title, article.summary]))

    response = prompt_sentiment_model(input_text, model)

    return response