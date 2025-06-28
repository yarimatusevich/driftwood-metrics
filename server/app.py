import json
from dataclasses import asdict

from finance_data import create_ticker_object, parse_ticker_data
from sentiment_model import get_sentiment_model
from llm import get_generative_ai_model, get_recommendation, write_llm_response_to_file

def main():
    repl()

def repl():
    sentiment_model = get_sentiment_model()
    llm_model = get_generative_ai_model()

    print("Models loaded")

    while True:
        ticker = input("Write a ticker: ")

        if ticker == "q": break

        ticker = create_ticker_object(ticker)
        stock_data = parse_ticker_data(ticker)

        print("Ticker data parsed")

        # Writes to file
        with open("output.json", "w") as f:
            json.dump(asdict(stock_data), f, indent=2)

        print("Output file updated")
        
        # Gets report from deepseek
        response = get_recommendation(stock_data, llm_model)
        write_llm_response_to_file(response)

        print("Response file updated")

if __name__ == "__main__":
    main()