from fastapi import FastAPI, Request
import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = FastAPI()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        send_message(chat_id, f"Bạn nói: {text}")

    return {"ok": True}