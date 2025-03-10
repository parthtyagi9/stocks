from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

@app.route('/')
def home():
    return jsonify({"message": "Stock Dashboard API is running!"})

if __name__ == "__main__":
    app.run(debug=True)
