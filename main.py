from fastapi import FastAPI, Request
import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = FastAPI()

# Lưu trạng thái đơn hàng tạm
orders = {}

# Gửi tin nhắn Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

# Xử lý tin nhắn + bán hàng
def handle_message(chat_id, text):
    text = text.lower()

    # tạo state nếu chưa có
    if chat_id not in orders:
        orders[chat_id] = {}

    order = orders[chat_id]

    # MENU
    if "menu" in text:
    return "🔥 NEW VERSION OK 🔥"

    # CHỌN MÓN
    if "cà phê" in text:
        order["item"] = "Cà phê"
        order["price"] = 20000
        return "Bạn muốn bao nhiêu ly cà phê?"

    if "trà sữa" in text:
        order["item"] = "Trà sữa"
        order["price"] = 25000
        return "Bạn muốn bao nhiêu ly trà sữa?"

    # SỐ LƯỢNG
    if text.isdigit() and "item" in order:
        qty = int(text)
        order["qty"] = qty
        total = qty * order["price"]
        order["total"] = total
        return f"Xác nhận: {order['item']} x{qty} = {total}đ\nGõ 'ok' để đặt"

    # XÁC NHẬN
    if text == "ok" and "total" in order:
        msg = f"✅ Đơn hàng:\n{order['item']} x{order['qty']} = {order['total']}đ\n\nChúng tôi sẽ giao sớm 🚀"
        
        # reset đơn
        orders.pop(chat_id)
        return msg

    return "Bạn cần gì? Gõ 'menu' để xem đồ uống ☕"

# Route test
@app.get("/")
def home():
    return {"status": "ok"}

# Webhook Telegram
@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = handle_message(chat_id, text)
        send_message(chat_id, reply)

    return {"ok": True}
    # force deploy
