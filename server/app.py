import json
from dataclasses import asdict
from sentiment_model import get_sentiment_model
from finance_data import create_ticker_object, parse_ticker_data

def main():
    repl()

def repl():
    sentiment_model = get_sentiment_model()

    while True:
        ticker = input("Write a ticker: ")

        if ticker == "q": break

        ticker = create_ticker_object(ticker)
        stock_data = parse_ticker_data(ticker)

        # Writes to file
        with open("output.json", "w") as f:
            json.dump(asdict(stock_data), f, indent=2)


if __name__ == "__main__":
    main()