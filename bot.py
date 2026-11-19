import os
import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

API = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

MENU = [
    ["🤖 چت با هوش مصنوعی", "🌍 ترجمه متن"],
    ["✍️ تولید متن", "🎮 بازی و سرگرمی"],
    ["🧩 معما و اطلاعات", "📢 کانال رسمی AI شو"],
    ["🏠 منوی اصلی"]
]

logging.basicConfig(level=logging.INFO)


def ask_ai(prompt):
    response = requests.post(
        API,
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "تو دستیار فارسی‌زبان و مفید ربات AI شو هستی."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_completion_tokens": 1200
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "chat"
    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )
    await update.message.reply_text(
        "سلام! به ربات هوشمند AI شو خوش اومدی 🤖\n\n"
        "از منوی زیر یکی از امکانات رو انتخاب کن.",
        reply_markup=keyboard
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "chat")

    if text == "📢 کانال رسمی AI شو":
        await update.message.reply_text("https://t.me/ai_sho_1")
        return

    if text == "🏠 منوی اصلی":
        context.user_data["mode"] = "chat"
        await start(update, context)
        return

    if text == "🤖 چت با هوش مصنوعی":
        context.user_data["mode"] = "chat"
        await update.message.reply_text("سؤالت رو بفرست تا جواب بدم.")
        return

    if text == "🌍 ترجمه متن":
        context.user_data["mode"] = "translate"
        await update.message.reply_text("متنت رو بفرست تا ترجمه کنم.")
        return

    if text == "✍️ تولید متن":
        context.user_data["mode"] = "write"
        await update.message.reply_text("بگو چه متنی برات بنویسم.")
        return

    if text == "🎮 بازی و سرگرمی":
        context.user_data["mode"] = "game"
        await update.message.reply_text(
            "🎯 بازی حدس عدد!\n"
            "یک عدد بین ۱ تا ۱۰ حدس بزن."
        )
        import random
        context.user_data["number"] = random.randint(1, 10)
        return

    if text == "🧩 معما و اطلاعات":
        context.user_data["mode"] = "riddle"
        await update.message.reply_text(
            "🧩 معما:\n"
            "آن چیست که هرچه از آن برداری بزرگ‌تر می‌شود؟"
        )
        return

    if mode == "game":
        if text.isdigit():
            guess = int(text)
            number = context.user_data.get("number")
            if guess == number:
                await update.message.reply_text("🎉 آفرین! درست حدس زدی.")
            else:
                await update.message.reply_text("نه! دوباره حدس بزن.")
            return

    if mode == "riddle":
        await update.message.reply_text(
            "جواب معما: گودال 😄\n"
            "برای معمای بعدی دوباره گزینه معما رو بزن."
        )
        return

    if mode == "translate":
        prompt = "متن زیر را به فارسی ترجمه کن:\n" + text
    elif mode == "write":
        prompt = "طبق درخواست زیر یک متن خوب فارسی بنویس:\n" + text
    else:
        prompt = text

    await update.message.reply_text("⏳ دارم آماده می‌کنم...")

    try:
        answer = await __import__("asyncio").to_thread(ask_ai, prompt)
        if not answer:
            answer = "پاسخی دریافت نشد. دوباره تلاش کن."
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i+4000])
    except Exception:
        logging.exception("AI request failed")
        await update.message.reply_text(
            "الان ارتباط با هوش مصنوعی برقرار نشد. کمی بعد دوباره امتحان کن."
        )


def main():
    if not TOKEN or not GROQ_KEY:
        raise ValueError("کلیدهای ربات پیدا نشدند.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()


if __name__ == "__main__":
    main()
