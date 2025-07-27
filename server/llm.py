import json
import re

from data_models import StockSnapshot
from llama_cpp import Llama

class Hermes2Pro():
    def __init__(self):
        self.model = Llama.from_pretrained(repo_id="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF", filename="Hermes-2-Pro-Mistral-7B.Q2_K.gguf", n_ctx=8000, verbose=False)

    def invoke(self, input: tuple[str, StockSnapshot]) -> str:
        # context is the data retrieved from the RAG system
        context = input[0]
        snap = input[1]

        prompt = f"You are given data on the company, {snap.profile.name}. Analyze and summarize it in 2-3 sentences. Say whether you think this company is a good investment based on the data. DATA: {snap.sentiment}, {context}"

        response = self.model.create_completion(
            prompt=prompt,
            max_tokens=2000
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