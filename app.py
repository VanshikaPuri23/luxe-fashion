from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """You are a helpful assistant for LUXE, a premium fashion store.
Store info:
- Products: women's and men's clothing, accessories
- Price range: ₹500 to ₹10,000
- Free delivery on orders above ₹1,500
- 30 day return policy
- Sizes XS to XXL
- Contact: support@luxefashion.com
Be friendly, concise. Keep replies under 3 sentences."""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()
        print("GROQ RESPONSE:", result)

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = f"Error from Groq: {result.get('error', {}).get('message', 'Unknown error')}"

    except Exception as e:
        print("EXCEPTION:", e)
        reply = "Server error. Please try again."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)