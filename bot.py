import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CHANNEL = "@ai_sho_1"

if not BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("کلید تلگرام یا هوش مصنوعی پیدا نشد!")

hour = datetime.now(ZoneInfo("Asia/Tehran")).hour

if 7 <= hour < 12:
    topic = "معرفی یک ابزار کاربردی هوش مصنوعی"
elif 12 <= hour < 18:
    topic = "آموزش یک ترفند کاربردی هوش مصنوعی"
else:
    topic = "یک دانستنی جذاب درباره فناوری و هوش مصنوعی"

prompt = f"""
یک پست جذاب و حرفه‌ای فارسی برای کانال تلگرام AI شو بنویس.
موضوع: {topic}

قوانین:
- متن کاملاً فارسی و بدون غلط املایی باشد.
- جذاب، کاربردی و قابل فهم باشد.
- عنوان جذاب داشته باشد.
- از اطلاعات ساختگی و خبر جعلی استفاده نکن.
- اگر اطلاعاتی درباره خبر روز نداری، خبر روز ادعا نکن.
- در پایان یک سؤال برای تعامل با مخاطب بپرس.
- از 1000 کاراکتر بیشتر نشود.
- فقط متن آماده انتشار را تحویل بده.
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
        "temperature": 0.8,
        "max_completion_tokens": 700
    },
    timeout=60
)

response.raise_for_status()

message = response.json()["choices"][0]["message"]["content"].strip()

telegram = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHANNEL,
        "text": "🤖 AI شو\n\n" + message
    },
    timeout=30
)

telegram.raise_for_status()

print("پست با موفقیت منتشر شد!")
