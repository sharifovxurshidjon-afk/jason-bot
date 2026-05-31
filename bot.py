import os
import requests
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

app = Flask(__name__)

def ask_ai(text):

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты умный AI ассистент как Jarvis. Отвечай как человек."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
    )

    result = response.json()

    print(result)

    if "choices" not in result:
        if "error" in result:
            return "AI временно перегружен. Попробуй через 30-60 секунд."
        return str(result)

    return result["choices"][0]["message"]["content"]


@app.route("/", methods=["POST"])
def webhook():

    data = request.json

    message = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]

    answer = ask_ai(message)

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": answer
        }
    )

    return "ok"


app.run(host="0.0.0.0", port=8080)
