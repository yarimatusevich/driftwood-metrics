from transformers import pipeline
from transformers.pipelines import TextClassificationPipeline

def get_sentiment_model():
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    return pipeline(model_name)

def analyze_sentiment(input_text: str, model: TextClassificationPipeline):
    return model(input_text)