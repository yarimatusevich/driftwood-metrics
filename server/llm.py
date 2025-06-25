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

TEMPLATE_REPORT_JSON = """
    You are a financial analyst. Based on the following stock data, return a JSON object that includes a summary of each key area and an overall investment recommendation.

    Return the result in exactly this format:

    {
    "valuation_summary": "...",
    "profitability_summary": "...",
    "balance_sheet_summary": "...",
    "growth_summary": "...",
    "performance_summary": "...",
    "analyst_sentiment_summary": "...",
    "article_sentiment_summary": "...",
    "overall_assessment": "..."
    }

    DATA:
    {data}

    Only return the JSON object. Do not include any explanations, markdown, or extra text.
"""

def get_recommendation(stock_data: StockData):
    prompt = TEMPLATE_REPORT_JSON.format(data = stock_data.jsonify())
    model_bundle = get_generative_ai_model()

    messages=[
        {
            'role': 'system',
            'content': "You are a financial analyst, using provided data create a structured JSON report either encouraging or discouraging clients from purchasing a stock depending on the data."
        },
        {
            'role': 'user',
            'content': f"Here is some stock data in the form of a JSON: {prompt}. Please analyze it and return a structured JSON recommendation."
        }
    ]

    return prompt_generative_ai_model(prompt, model_bundle, messages)

def get_generative_ai_model() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("cpu")

    return tokenizer, model 

# def prompt_generative_ai_model(
#         input: str,
#         model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase],
#         messages: list[dict]
#         ) -> dict:
        
#     model, tokenizer = model_bundle

    # messages=[
    #     {
    #         'role': 'system',
    #         'content': "You are a financial analyst, using provided data create a structured JSON report either encouraging or discouraging clients from purchasing a stock depending on the data."
    #     },
    #     {
    #         'role': 'user',
    #         'content': f"Here is some stock data: { ... }. Please analyze it and return a structured JSON recommendation."
    #     }
    # ]


def prompt_generative_ai_model(
        prompt: str,
        model_bundle: tuple[AutoModelForCausalLM, PreTrainedTokenizerBase],
        messages: list[dict]
        ) -> dict:
    tokenizer, model = model_bundle

    input_ids = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        return_tensors="pt",
        add_generation_prompt=True
    ).to(model.device)

    output = model.generate(input_ids, max_new_tokens=100)

    return tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True)