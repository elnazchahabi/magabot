from aiogram import Router, types
from aiogram.filters import Command
from megabot.modules.dashboard.stats import gather_stats
from megabot.modules.dashboard.plots import generate_stats_plot

router = Router()

@router.message(Command("stats"))
async def send_stats(message: types.Message):
    user_count, msg_count, order_count = await gather_stats()
    generate_stats_plot(user_count, msg_count, order_count)
    await message.answer_photo(types.FSInputFile("stats.png"), caption="📊 آمار فعلی")
