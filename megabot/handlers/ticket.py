from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from megabot.config import ADMINS
from megabot.database.tickets import (
    create_ticket, get_all_open_tickets,
    answer_ticket, get_ticket_by_id
)
from megabot.keyboards.ticket import ticket_admin_buttons

router = Router()

# --- ثبت تیکت ---
class TicketState(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()

@router.message(Command("ticket"))
async def ask_ticket(message: types.Message, state: FSMContext):
    await message.answer("لطفاً سوال یا مشکل خود را بنویسید:")
    await state.set_state(TicketState.waiting_for_question)

@router.message(TicketState.waiting_for_question)
async def save_ticket(message: types.Message, state: FSMContext):
    ticket_id = await create_ticket(message.from_user.id, message.text)
    await message.answer("✅ تیکت شما ثبت شد. پشتیبانی به زودی پاسخ می‌دهد.")
    await state.clear()

    # ارسال نوتیف برای ادمین
    for admin in ADMINS:
        await message.bot.send_message(
            admin,
            f"📩 تیکت جدید #{ticket_id}:\n{message.text}",
            reply_markup=ticket_admin_buttons(ticket_id)
        )

# --- ادمین پاسخ می‌دهد ---
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply_init(callback: types.CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.split("_")[1])
    await state.set_state(TicketState.waiting_for_answer)
    await state.update_data(ticket_id=ticket_id)
    await callback.message.answer("📝 پاسخ خود را بنویسید:")

@router.message(TicketState.waiting_for_answer)
async def send_admin_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data["ticket_id"]

    ticket = await get_ticket_by_id(ticket_id)
    if not ticket:
        await message.answer("❌ تیکت یافت نشد.")
        return

    await answer_ticket(ticket_id, message.text)
    await message.answer("✅ پاسخ ثبت شد و تیکت بسته شد.")
    await message.bot.send_message(
        ticket.user_id,
        f"🟢 پاسخ به تیکت شما:\n{message.text}"
    )
    await state.clear()
