# handlers/base.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from database.models import add_user

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user
    add_user(user.id, user.full_name, user.username)
    await message.answer(f"سلام {user.full_name} 👋\nبه Mega Bot خوش اومدی!")
