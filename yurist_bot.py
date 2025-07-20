import telebot
import openai
import os

# Muhit o'zgaruvchilardan kalitlarni o'qish (Render uchun qulay)
TELEGRAM_BOT_TOKEN = os.environ.get("7505715870:AAEopIKBJcfbW3mvpS6vZ7_BnfesoSFN_PQ")
OPENAI_API_KEY = os.environ.get("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")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN topilmadi. Render environment variables ga qo'shing.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY topilmadi. Render environment variables ga qo'shing.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(
        message,
        "👋 Salom! Men AI Yuristman.\n"
        "Menga huquqiy savolingizni yozing (mehnat, jinoyat, fuqarolik, ma'muriy, mulk, va boshqalar).\n"
        "Misol: 'Ishdan ogohlantirmasdan bo'shatish qonuniymi?'"
    )

@bot.message_handler(func=lambda message: True)
def ai_javob(message):
    savol = message.text.strip()
    try:
        # OpenAI'ga so'rov
        javob = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,  # aniqroq, rasmiyroq javoblar
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Siz O'zbekiston Respublikasi qonunchiligi bo'yicha javob beruvchi yurist AI botsiz. "
                        "Foydalanuvchi savollariga qisqa, tushunarli, rasmiy va huquqiy asosli javob bering. "
                        "Mavjud bo'lsa: JK, MJtK, Fuqarolik kodeksi, Mehnat kodeksi, JPK va boshqa tegishli hujjatlardan misollar keltiring. "
                        "Qonun matnini so'zma-so'z ko'chirmang; qisqacha sharh, modda raqami va tavsiya bering."
                    )
                },
                {"role": "user", "content": savol}
            ],
            max_tokens=600
        )
        natija = javob["choices"][0]["message"]["content"].strip()

    except Exception as e:
        natija = "❌ Xatolik: " + str(e)

    bot.reply_to(message, natija)

if __name__ == "__main__":
    print("🤖 Yurist bot ishga tushyapti...")
    bot.infinity_polling(skip_pending=True)
