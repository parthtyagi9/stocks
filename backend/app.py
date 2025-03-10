from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app) 

VALID_PERIODS = {
    '1d': '1d',
    '5d': '5d',
    '1mo': '1mo',
    '3mo': '3mo',
    '6mo': '6mo',
    'ytd': 'ytd',
    '1y': '1y',
    '2y': '2y',
    '5y': '5y',
    'max': 'max'
}

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


# Dummy prediction button
@app.route('/api/stocks/<string:ticker>/predict', methods=['POST'])
def get_predictions(ticker):
    prediction = {
        "ticker": ticker.upper(),
        "prediction": "Bullish",
        "confidence": 0.9
    }
    return jsonify(prediction)


@app.route('/api/stocks/<string:ticker>/historical/<string:period>')
def get_historical(ticker, period):
    if period not in VALID_PERIODS:
        return jsonify({"error": f"Invalid period. Choose from {VALID_PERIODS}"}), 400

    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    if history.empty:
        return jsonify({"error": "No data found"}), 404

    history.reset_index(inplace=True)
    history['Date'] = history['Date'].dt.strftime('%Y-%m-%d')

    data = history.to_dict(orient="records")

    return jsonify({
        "ticker": ticker.upper(),
        "period": period,
        "historical": data
    })


# Ensure the app runs correctly
if __name__ == "__main__":
    app.run(debug=True)
