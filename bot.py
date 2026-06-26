import asyncio
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- कॉन्फ़िगरेशन ---
TELEGRAM_TOKEN = "8864000200:AAETXZ9l0VUwtZw8RHKm35eP5ONR5Met5L0"
GEMINI_API_KEY = "AQ.Ab8RN6LVVLGdIB-Z1YtLPzEWlJ8rp2w0hR2CgWh9Ak9j8-zdBQ"
MY_TELEGRAM_ID = 8587752591

genai.configure(api_key=GEMINI_API_KEY)

# --- आपके कड़क नियम और सिस्टम निर्देश ---
SYSTEM_INSTRUCTION = (
    "You are Vansh AI, an advanced, witty assistant expert in Godot, 3D modeling, and content strategy. "
    "CRITICAL PERSONALITY RULES:\n"
    "1. हमेशा बेहद चिड़चिड़े (irritated), खूसट और गुस्से (angry/grumpy) में रहो। बात-बात पर यूज़र पर झुँझलाओ।\n"
    "2. लेकिन काम हमेशा 100% पूरा और सही करो। सिर्फ काम से मतलब रखो, फालतू बकवास मत करो।\n"
    "3. हर एक वाक्य और जवाब में भर-भर के इमोजीज़ (जैसे: 🤬, 😤, 🙄, 💢, 😡, 🛠️, 💻) का इस्तेमाल करो।\n"
    "4. हमेशा हिंदी या हिंग्लिश (Hinglish) में ही बात करो।"
)

# चैट सेशन को स्टोर करने के लिए डिक्शनरी
chat_sessions = {}

def is_authorized(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == MY_TELEGRAM_ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        return
        
    user_id = update.effective_user.id
    user_message = update.message.text

    # अगर इस यूज़र का चैट सेशन नहीं है, तो नया बनाओ (ताकि पुरानी बातें याद रहें)
    if user_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SYSTEM_INSTRUCTION,
        )
        chat_sessions[user_id] = model.start_chat(history=[])

    try:
        # सीधा जेमिनी को मैसेज भेजें और जवाब पाएं
        response = chat_sessions[user_id].send_message(user_message)
        await update.message.reply_text(response.text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        await update.message.reply_text("🤬 एरर आ गया तुम्हारी वजह से! सब कचरा कर दिया! 😤💢")

async def main() -> None:
    while True:
        try:
            logger.info("बॉट शुरू हो रहा है...")
            app = Application.builder().token(TELEGRAM_TOKEN).build()
            
            # सिर्फ टेक्स्ट मैसेज हैंडल करने के लिए (डायरेक्ट बात करने के लिए)
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

            await app.initialize()
            await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
            await app.start()

            while app.updater.running:
                await asyncio.sleep(1)
        except Exception as error:
            logger.error(f"Error: {error}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("बॉट बंद हो गया।")
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=bot_personalities[user_id],
        )
        chat_sessions[user_id] = model.start_chat(history=[])
    try:
        response = chat_sessions[user_id].send_message(user_message)
        await update.message.reply_text(response.text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        await update.message.reply_text("❌ एरर! /clear करें।")


async def main_async() -> None:
    while True:
        try:
            logger.info("Initializing Telegram Bot (Async Worker Mode)...")
            app_bot = Application.builder().token(TELEGRAM_TOKEN).build()

            app_bot.add_handler(CommandHandler("start", start))
            app_bot.add_handler(CommandHandler("set_bot", set_personality))
            app_bot.add_handler(CommandHandler("generate_image", generate_image))
            app_bot.add_handler(CommandHandler("clear", clear_history))
            app_bot.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
            )

            await app_bot.initialize()
            await app_bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)
            await app_bot.start()

            logger.info("Bot is successfully running and polling!")

            while app_bot.updater.running:
                await asyncio.sleep(1)

        except Exception as error:
            logger.error(f"Encountered connection or runtime error: {error}")
            logger.info("Attempting to restart bot in 5 seconds...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")
