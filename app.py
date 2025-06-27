from flask import Flask, request, jsonify
import requests

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
    print("💬 받은 데이터:", data)  # <- 요청 데이터 확인용

    # 일단 기본 메시지 지정
    user_message = "안녕하세요. 무엇을 도와드릴까요?"

    # utterance가 존재하면 그걸 사용
    if data and "userRequest" in data and "utterance" in data["userRequest"]:
        user_message = data["userRequest"]["utterance"]

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



@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("💬 받은 요청 데이터:", data)

        user_message = data.get("userRequest", {}).get("utterance", "안녕하세요!")

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

    except Exception as e:
        print("❌ 오류 발생:", str(e))  # ← 여기가 핵심!
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "⚠️ 서버 오류가 발생했어요."
                    }
                }]
            }
        }), 500
