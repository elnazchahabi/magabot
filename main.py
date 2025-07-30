import asyncio
from megabot.bot import bot, dp
from megabot.database.db import init_db
from megabot.handlers import start, help
from megabot.utils.logger import setup_logger
from megabot.middlewares.message_logger import MessageLoggerMiddleware
from megabot.middlewares.anti_spam import AntiSpamMiddleware
from megabot.handlers import shop
from megabot.handlers import ticket

from megabot.handlers import ai_handler
from megabot.handlers import quiz_handler, admin_dashboard_handler






async def main():
    setup_logger()
    await init_db()

    # فقط یکبار
    dp.update.middleware.register(MessageLoggerMiddleware())
    dp.update.middleware.register(AntiSpamMiddleware())

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(shop.router)
    dp.include_router(ticket.router)
    dp.include_router(ai_handler.router)
    dp.include_router(quiz_handler.router)
    dp.include_router(admin_dashboard_handler.router)

    print("✅ Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
