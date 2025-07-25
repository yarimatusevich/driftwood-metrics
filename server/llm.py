import json
import re

from data_models import StockSnapshot
from llama_cpp import Llama

class Hermes2Pro():
    def __init__(self):
        self.model = Llama.from_pretrained(repo_id="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF", filename="Hermes-2-Pro-Mistral-7B.Q2_K.gguf", n_ctx=8000, verbose=False)

    def invoke(self, input: StockSnapshot) -> str:
        prompt = f"Summarize this data in two sentences. In your summary describe if this company is a good invesment. Here is the data: {input.financials}, {input.sentiment}"

        response = self.model.create_completion(
            prompt=prompt,
            max_tokens=1000
        )

        return response["choices"][0]["text"]

"""
TODO: Decide whether to remove or keep
"""
def parse_model_response_into_dict(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'{.*}', response, re.DOTALL)

    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("No valid JSON found in model output")