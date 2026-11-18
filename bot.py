
import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@ai_sho_1"

message = "🤖 سلام! ربات AI شو با موفقیت فعال شد."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(url, data={
    "chat_id": CHANNEL,
    "text": message
})

print(response.text)
response.raise_for_status()
