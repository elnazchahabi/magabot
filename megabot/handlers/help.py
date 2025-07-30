from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        "<b>دستورهای ربات:</b>\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "ارسال پیام و دریافت پاسخ از بات"
    )
