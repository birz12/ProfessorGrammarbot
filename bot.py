import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# الإعدادات
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "أنت أستاذ قواعد إنجليزية محترف. صحح الأخطاء وأجب على الأسئلة بوضوح وبطريقة تعليمية."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("عذراً، حدث خطأ، يرجى المحاولة لاحقاً.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
