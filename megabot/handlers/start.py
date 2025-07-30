from aiogram import Router, types
from aiogram.filters import CommandStart
from megabot.database.models import add_user_if_not_exists

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user
    await add_user_if_not_exists(user.id, user.full_name, user.username)
    await message.answer(f"سلام {user.full_name} 👋\nبه Mega Bot خوش اومدی!")
