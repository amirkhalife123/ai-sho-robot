
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@ai_sho_1"

if not TOKEN:
    raise ValueError("توکن ربات در تنظیمات مخزن پیدا نشد!")

message = "🤖 سلام! ربات AI شو با موفقیت فعال شد."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHANNEL,
        "text": message
    },
    timeout=30
)

print("پاسخ تلگرام:", response.text)
response.raise_for_status()
