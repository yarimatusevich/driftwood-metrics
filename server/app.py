from flask import Flask, jsonify
from flask_cors import CORS

from finance_data import create_ticker_object, parse_ticker_data
from llm import get_generative_ai_model, get_recommendation, parse_model_response_into_dict, write_llm_response_to_file

app = Flask(__name__)
CORS(app)

@app.route('/quote/<ticker>', methods=['GET'])
def get_quote(ticker: str):
    # Initializes deepseek
    deepseek_model_and_tokenizer = get_generative_ai_model()

    # Creates a ticker object containing data parsed from Yahoo Finance using provided ticker
    ticker_data = create_ticker_object(ticker)

    # Parses ticker data into a stock data object
    stock_data = parse_ticker_data(ticker_data)

    # Gets model reponse
    response = get_recommendation(stock_data, deepseek_model_and_tokenizer)

    # Parses model response into a dict
    response_dict = parse_model_response_into_dict(response)

    return jsonify(response_dict)

if __name__ == "__main__":
    app.run(debug=True)