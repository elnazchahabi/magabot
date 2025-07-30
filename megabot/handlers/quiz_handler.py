from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery
from megabot.modules.game.quiz import send_question, validate_answer
from megabot.database.users import update_user_score

router = Router()

@router.message(Command("quiz"))
async def quiz_command(message: types.Message):
    await send_question(message)

@router.callback_query(lambda c: c.data.startswith("answer:"))
async def handle_answer(callback: CallbackQuery):
    selected = callback.data.split(":")[1]
    user_id = callback.from_user.id
    if validate_answer(user_id, selected):
        await update_user_score(user_id, 1)
        await callback.message.answer("✅ درست بود!")
    else:
        await callback.message.answer("❌ اشتباه بود!")
    await send_question(callback.message)
