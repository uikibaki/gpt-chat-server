from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = "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"

def ask_gpt(message):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    try:
        user_message = data.get("userRequest", {}).get("utterance", "")
    except:
        user_message = "질문이 전달되지 않았어요."

    gpt_reply = ask_gpt(user_message)
    
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": gpt_reply
                }
            }]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
