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
        print("✅ GPT 응답:", res_json)

        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"❌ GPT 응답 오류: {res_json.get('error', {}).get('message', 'Unknown error')}"

    except Exception as e:
        print("❌ GPT 요청 실패:", str(e))
        return "⚠️ GPT 호출 중 오류가 발생했어요."
