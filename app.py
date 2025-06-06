from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import logging

# Load environment variables (make sure to set GROQ_API_KEY in environment)
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
CORS(app)  # Allow all origins, adjust if needed

logging.basicConfig(level=logging.INFO)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    app.logger.info(f"Received message: {data.get('message')}")

    try:
        if not data or "message" not in data:
            raise ValueError("Missing 'message' in request data")

        user_message = data["message"]
        app.logger.info(f"Processing message: {user_message}")

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            app.logger.info(f"API response: {reply}")
            app.logger.info(f"Returning reply: {reply}")
            return jsonify({"reply": reply})
        else:
            error_msg = f"Groq API error: {response.text}"
            app.logger.error(error_msg)
            return jsonify({"error": "API Error", "details": error_msg}), 500

    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)

