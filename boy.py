import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

logging.basicConfig(level=logging.INFO)

TOKEN = "8574908146:AAGmKFBlYBxWyMjatnrppH_9Zd0tB1NoHd4"

WAITING_PROBLEM = 1
WAITING_OFFER = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Создать заявку")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Это бот обмена помощью.\n\n"
        "Ты описываешь свою проблему или желание — и предлагаешь что-то взамен.\n\n"
        "Нажми кнопку, чтобы начать 👇",
        reply_markup=markup
    )

async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Шаг 1 из 2*\n\n"
        "Опиши свою проблему или желание.\n"
        "Например: _«Хочу научиться делать сайты»_ или _«Нужна помощь с переездом»_\n\n"
        "Пиши в свободной форме и нажми отправить ✉️",
        parse_mode="Markdown"
    )
    return WAITING_PROBLEM

async def receive_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["problem"] = update.message.text
    await update.message.reply_text(
        "✅ Принято!\n\n"
        "🎁 *Шаг 2 из 2*\n\n"
        "А что ты предлагаешь взамен?\n"
        "Это может быть что угодно: оригами, пачка чипсов, урок по гитаре, совет, улыбка 😄\n\n"
        "Опиши в свободной форме и нажми отправить ✉️",
        parse_mode="Markdown"
    )
    return WAITING_OFFER

async def receive_offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = context.user_data.get("problem", "—")
    offer = update.message.text
    user = update.message.from_user
    name = user.first_name or "Аноним"
    username = f"@{user.username}" if user.username else "нет username"

    card = (
        f"🗂 *Новая заявка*\n\n"
        f"👤 *Автор:* {name} ({username})\n\n"
        f"❓ *Проблема / желание:*\n{problem}\n\n"
        f"🎁 *Предлагает взамен:*\n{offer}"
    )

    keyboard = [[KeyboardButton("🚀 Создать заявку")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"🎉 Твоя заявка готова!\n\n{card}\n\n"
        "Хочешь создать ещё одну? Нажми кнопку 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Создать заявку")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "❌ Отменено. Можешь начать заново 👇",
        reply_markup=markup
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", new_request),
            MessageHandler(filters.Regex("^🚀 Создать заявку$"), new_request)
        ],
        states={
            WAITING_PROBLEM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_problem)
            ],
            WAITING_OFFER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_offer)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
