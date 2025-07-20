import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os

# OpenAI API kaliti
openai.api_key = os.getenv("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")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Savolingizni yuboring.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Siz advokatsiz. Huquqiy masalalarga javob berasiz."},
            {"role": "user", "content": user_input}
        ]
    )

    answer = response['choices'][0]['message']['content']
    await update.message.reply_text(answer)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()
