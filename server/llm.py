"""
llm_prompt.py

This module handles interaction with the generative language model (e.g., DeepSeek).

It includes functions to:
- Load a causal language model and tokenizer (e.g., DeepSeek Coder Instruct)
- Format structured financial data into prompts
- Generate a structured JSON report with investment recommendations

This is used to interpret financial metrics and summarize them into human-readable, machine-parseable reports.
"""

"""
Returns an instance of DeepSeek coder model. 
Using the instruct version as this model is tailored towards creating structured responses,
 which will be needed when integrating the frontend with the backend.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerBase, PreTrainedModel
from data_models import StockData
import torch

def get_generative_ai_model() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("mps")

    return tokenizer, model 

# def get_generative_ai_model() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
#     model_name = "microsoft/phi-2"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name,  torch_dtype= torch.float16).to("mps")

#     return tokenizer, model 

def prompt_generative_ai_model(messages: list[dict], model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase]) -> dict:
    tokenizer, model = model_bundle

    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True
    ).to(model.device)

    output = model.generate(input_ids, max_new_tokens=100)

    return tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True)

def get_prompt(stock_data: StockData) -> str:
    return f"""
    You are a financial analyst. Based on the following data, return a JSON object in this format:

    {{
    "valuation_summary": "...",
    "profitability_summary": "...",
    "balance_sheet_summary": "...",
    "growth_summary": "...",
    "performance_summary": "...",
    "analyst_sentiment_summary": "...",
    "article_sentiment_summary": "...",
    "overall_assessment": "..."
    }}

    DATA:
    {stock_data.jsonify()}

    Only return the JSON object.
    """

def get_recommendation(stock_data: StockData, model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase]):
    prompt = get_prompt(stock_data)

    messages=[
        {
            'role': 'system',
            'content': "You are a financial analyst."
        },
        {
            'role': 'user',
            'content': f"{prompt}."
        }
    ]

    return prompt_generative_ai_model(messages, model_bundle)