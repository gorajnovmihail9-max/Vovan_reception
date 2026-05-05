import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TOKEN = "8681362491:AAEBlNlFTleUrHuXDRRuE-oXPl2tXc7NVgs"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    problem = State()
    offer = State()

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.KeyboardButton("🚀 Создать заявку"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 Привет! Опиши свою проблему или желание — и предложи что-то взамен.\n\nНажми кнопку чтобы начать 👇", reply_markup=kb)

@dp.message_handler(text="🚀 Создать заявку")
async def new_request(message: types.Message):
    await Form.problem.set()
    await message.answer("📝 Шаг 1 из 2\n\nОпиши свою проблему или желание и нажми отправить ✉️")

@dp.message_handler(state=Form.problem)
async def receive_problem(message: types.Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await Form.offer.set()
    await message.answer("✅ Принято!\n\n🎁 Шаг 2 из 2\n\nЧто предлагаешь взамен? Это может быть что угодно — нажми отправить ✉️")

@dp.message_handler(state=Form.offer)
async def receive_offer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    problem = data.get("problem", "—")
    offer = message.text
    name = message.from_user.first_name or "Аноним"
    username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
    card = f"🗂 Новая заявка\n\n👤 Автор: {name} ({username})\n\n❓ Проблема/желание:\n{problem}\n\n🎁 Предлагает взамен:\n{offer}"
    await state.finish()
    await message.answer(f"🎉 Готово!\n\n{card}", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
