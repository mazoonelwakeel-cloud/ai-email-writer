from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_email():
    try:
        data = request.json

        purpose = data["purpose"]
        recipient = data["recipient"]
        sender = data["sender"]
        language = data["language"]
        tone = data["tone"]
        length = data["length"]

        prompt = f"""
Write a {length} email in {language}.

Purpose: {purpose}
Recipient: {recipient}
Tone: {tone}
Sender: {sender}

Only write the email.
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta/llama-3.1-8b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500
        }

        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        result = response.json()

        if "choices" not in result:
            return jsonify({
                "success": False,
                "error": str(result)
            })

        email = result["choices"][0]["message"]["content"]

        return jsonify({
            "success": True,
            "email": email
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)