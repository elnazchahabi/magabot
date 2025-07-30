from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from megabot.database.warnings import increase_warning

BAD_WORDS = {"فحش", "بد", "spam"}

class AntiSpamMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        text = event.text or ""
        if any(word in text.lower() for word in BAD_WORDS):
            warnings = await increase_warning(event.from_user.id)
            if warnings >= 3:
                await event.answer("⛔ شما بن شدید به دلیل تکرار تخلف!")
                return
            await event.answer(f"⚠️ این پیام مجاز نیست (تعداد اخطارها: {warnings})")
            return
        return await handler(event, data)
