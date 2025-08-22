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
 
        prompt = f"""
        You are given data on the company: {snap.profile.name}.
        Here is the top ten most recent article sentiments about the company: {snap.sentiment}
        Here is a summary of historical sentiment: {context}
        
        Only respond with JSON formatted string with no explanations or any other dicussion in this format:

        ```json
        {{
        "decision": "buy" | "sell" | "hold",
        "reasoning": "one sentence summary of why, based on the data"
        }}
        """

        response = self.model.create_completion(
            prompt=prompt,
            max_tokens=300
        )

        clean_response = parse_model_response_into_dict(response=response["choices"][0]["text"])

        return clean_response

def parse_model_response_into_dict(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'{.*}', response, re.DOTALL)

    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("No valid JSON found in model output")