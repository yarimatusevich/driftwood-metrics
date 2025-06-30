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

import re
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerBase, PreTrainedModel
from data_models import StockData

def get_generative_ai_model() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("cuda")

    return tokenizer, model 

def prompt_generative_ai_model(messages: list[dict], model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase]) -> dict:
    tokenizer, model = model_bundle

    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True
    ).to(model.device)

    output = model.generate(input_ids, max_new_tokens=1000, temperature=0.0, do_sample=False)

    return tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True)

def get_prompt(stock_data: StockData) -> str:
    return f"""
    Using this data: {stock_data.jsonify()}, summarize it and,
    return a structured json with the following fields:
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
    """

def get_recommendation(stock_data: StockData, model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase]):
    prompt = get_prompt(stock_data)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial analyst. "
                "Respond only with a valid JSON object. "
                "Do not include any explanations, headings, or extra text."
                "Specifically mention risks and downsides, do not be afraid to be negative"
            )
        },
        {
            "role": "user",
            "content": f"{prompt.strip()}."
        }
    ]

    return prompt_generative_ai_model(messages, model_bundle)

def parse_model_response_into_dict(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'{.*}', response, re.DOTALL)

    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("No valid JSON found in model output")

def write_llm_response_to_file(response: dict):
    with open("response.json", "w") as f:
        f.write(parse_model_response_into_dict(response))