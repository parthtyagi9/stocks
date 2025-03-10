from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return jsonify({"message": "Stock Dashboard API is running!"})

@app.route('/api/stocks/<string:ticker>')
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    price = stock.info.get("regularMarketPrice")
    name = stock.info.get("longName")
    if price is None:
        return jsonify({"error": "Ticker not found"}), 404
    return jsonify({
        "ticker": ticker.upper(),
        "name": name,
        "price": price
    })

# making a dummy prediction button
@app.route('api/stocks/<string:ticker>/preidct', methods=['POST'])
def get_predictions(ticker):
    prediction = {
        "ticker": ticker.upper(),
        "prediction": "Bullish",
        "confidence": 0.9
    }
    return jsonify(prediction)


if __name__ == "__main__":
    app.run(debug=True)
