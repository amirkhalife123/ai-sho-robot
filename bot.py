
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CHANNEL = "@ai_sho_1"

if not BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("کلیدهای ربات یا هوش مصنوعی پیدا نشدند!")

hour = datetime.now(ZoneInfo("Asia/Tehran")).hour

if 7 <= hour < 12:
    topic = "معرفی یک ابزار کاربردی هوش مصنوعی"
elif 12 <= hour < 18:
    topic = "آموزش یک ترفند کاربردی هوش مصنوعی"
else:
    topic = "دانستنی جذاب درباره فناوری و هوش مصنوعی"

prompt = f"""
برای کانال تلگرام AI شو یک پست فارسی جذاب بنویس.

موضوع: {topic}

شرایط:
- عنوان جذاب داشته باش.
- متن کاربردی و قابل فهم باشد.
- حداقل 150 و حداکثر 700 کاراکتر باشد.
- بدون غلط املایی باشد.
- اطلاعات ساختگی منتشر نکن.
- در پایان یک سؤال از مخاطب بپرس.
- فقط متن نهایی پست را بنویس.
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "reasoning_effort": "low",
        "temperature": 0.7,
        "max_completion_tokens": 2048
    },
    timeout=90
)

response.raise_for_status()

result = response.json()
choice = result["choices"][0]
message = choice["message"].get("content")

if not message or not message.strip():
    raise ValueError(
        f"متن هوش مصنوعی خالی است. "
        f"پایان پاسخ: {choice.get('finish_reason')}"
    )

message = message.strip()

telegram = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHANNEL,
        "text": "🤖 AI شو\n\n" + message
    },
    timeout=30
)

telegram.raise_for_status()

print("پست با موفقیت تولید و منتشر شد!")
print("موضوع:", topic)
print("تعداد کاراکتر:", len(message))
