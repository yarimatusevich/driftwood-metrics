# from flask import Flask, jsonify
# from flask_cors import CORS
from stock_data import get_data_from_ticker, parse_data
from sentiment_analyzer import get_sentiment_model, analyze_article_sentiment

# app = Flask(__name__)
# CORS(app)

# @app.route("/", methods = ["Get"])
def main():
    sentiment_model = get_sentiment_model()

    # REPL
    while True:
        ticker = input("Write a ticker: ")

        if ticker == "q": break

        data = get_data_from_ticker(ticker)
        parsed_data = parse_data(data)

        for i, data in enumerate(parsed_data):
            sentiment = analyze_article_sentiment(data, sentiment_model)
            print(f"{i}. {data.title}: {sentiment}")

if __name__ == "__main__":
    # app.run(port = 8080)
    main()