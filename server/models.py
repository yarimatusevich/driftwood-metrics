from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

def get_sentiment_model() -> :
    model_name = "ProsusAI/finbert"
    return pipeline(model = model_name)

"""
Returns an instance of DeepSeek coder model. 
Using the instruct version as this model is tailored towards creating structured responses,
 which will be needed when integrating the frontend with the backend.
"""
def get_gen_ai() -> :
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("cpu")

    return tokenizer, model 

