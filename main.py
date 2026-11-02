import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": user_text}]
        )
        reply_text = response.content[0].text
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot Telegram Claude aktif di Koyeb!")
    app.run_polling()
