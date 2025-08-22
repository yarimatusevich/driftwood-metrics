from flask import Flask, jsonify
from flask_cors import CORS

from pipelines import create_pipeline

app = Flask(__name__)
CORS(app)

@app.route('/quote/<ticker>', methods=['GET'])
def get_quote(ticker: str):
    pipeline = create_pipeline()
    response = pipeline.invoke(ticker)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)