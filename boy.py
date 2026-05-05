import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "8681362491:AAGdfNaFG40U-A6fmBjC074fKifJU-h-tcA"

WAITING_PROBLEM = 1
WAITING_OFFER = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Создать заявку")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Опиши свою проблему или желание — и предложи что-то взамен.\n\nНажми кнопку чтобы начать 👇",
        reply_markup=markup
    )

async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Шаг 1 из 2\n\nОпиши свою проблему или желание и нажми отправить ✉️")
    return WAITING_PROBLEM

async def receive_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["problem"] = update.message.text
    await update.message.reply_text("✅ Принято!\n\n🎁 Шаг 2 из 2\n\nЧто предлагаешь взамен? Это может быть что угодно — нажми отправить ✉️")
    return WAITING_OFFER

async def receive_offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = context.user_data.get("problem", "—")
    offer = update.message.text
    user = update.message.from_user
    name = user.first_name or "Аноним"
    username = f"@{user.username}" if user.username else "нет username"
    card = f"🗂 Новая заявка\n\n👤 Автор: {name} ({username})\n\n❓ Проблема/желание:\n{problem}\n\n🎁 Предлагает взамен:\n{offer}"
    keyboard = [[KeyboardButton("🚀 Создать заявку")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(f"🎉 Готово!\n\n{card}", reply_markup=markup)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отменено.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", new_request),
            MessageHandler(filters.Regex("^🚀 Создать заявку$"), new_request)
        ],
        states={
            WAITING_PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_problem)],
            WAITING_OFFER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_offer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
