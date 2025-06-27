from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_KEY = "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"

def ask_gpt(message):
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}]
            }
        )

        res_json = response.json()
        print("✅ GPT 응답:", res_json)  # 👈 이 줄 꼭 있어야 해!

        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"❌ GPT 응답 오류: {res_json.get('error', {}).get('message', 'Unknown error')}"

    except Exception as e:
        print("❌ GPT 요청 실패:", str(e))
        return "⚠️ GPT 호출 중 오류가 발생했어요."

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
        print("❌ 전체 처리 실패:", str(e))
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "서버 오류가 발생했어요. 다시 시도해주세요."
                    }
                }]
            }
        }), 500


# 🔥 반드시 있어야 하는 부분!
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
