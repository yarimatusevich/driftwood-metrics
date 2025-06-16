from stock_data import Article
from transformers import pipeline
from transformers.pipelines import TextClassificationPipeline

def get_sentiment_model():
    model_name = "ProsusAI/finbert"
    return pipeline(model = model_name, return_all_scores = True)

def analyze_article_sentiment(article: Article, model: TextClassificationPipeline):
    # filters out null, joins with space
    input_text = " ".join(filter(None, [article.title, article.summary]))
    return model(input_text)