import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

TOKEN = "8681362491:AAGdfNaFG40U-A6fmBjC074fKifJU-h-tcA"

class Form(StatesGroup):
    problem = State()
    offer = State()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Создать заявку")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Опиши свою проблему или желание — и предложи что-то взамен.\n\nНажми кнопку чтобы начать 👇", reply_markup=kb)

@dp.message(F.text == "🚀 Создать заявку")
async def new_request(message: Message, state: FSMContext):
    await message.answer("📝 Шаг 1 из 2\n\nОпиши свою проблему или желание и нажми отправить ✉️")
    await state.set_state(Form.problem)

@dp.message(Form.problem)
async def receive_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await message.answer("✅ Принято!\n\n🎁 Шаг 2 из 2\n\nЧто предлагаешь взамен? Это может быть что угодно — нажми отправить ✉️")
    await state.set_state(Form.offer)

@dp.message(Form.offer)
async def receive_offer(message: Message, state: FSMContext):
    data = await state.get_data()
    problem = data.get("problem", "—")
    offer = message.text
    name = message.from_user.first_name or "Аноним"
    username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
    card = f"🗂 Новая заявка\n\n👤 Автор: {name} ({username})\n\n❓ Проблема/желание:\n{problem}\n\n🎁 Предлагает взамен:\n{offer}"
    await state.clear()
    await message.answer(f"🎉 Готово!\n\n{card}", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
