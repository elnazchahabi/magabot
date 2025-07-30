# megabot/modules/game/quiz.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from megabot.database.users import update_user_score, get_user_score

QUESTIONS = [
    {
        "question": "پایتخت ایران کجاست؟",
        "options": ["تهران", "مشهد", "اصفهان"],
        "answer": "تهران"
    },
    {
        "question": "۲ × ۵ چند می‌شود؟",
        "options": ["۱۰", "۱۵", "۲۰"],
        "answer": "۱۰"
    },
]

user_quiz_index = {}

async def send_question(message: types.Message):
    user_id = message.from_user.id
    index = user_quiz_index.get(user_id, 0)
    if index >= len(QUESTIONS):
        await message.answer("🎉 مسابقه تمام شد! امتیاز شما: {}".format(await get_user_score(user_id)))
        return

    question = QUESTIONS[index]
    kb = InlineKeyboardBuilder()
    for opt in question["options"]:
        kb.button(text=opt, callback_data=f"answer:{opt}")
    await message.answer(question["question"], reply_markup=kb.as_markup())

def validate_answer(user_id, selected):
    index = user_quiz_index.get(user_id, 0)
    if index < len(QUESTIONS):
        correct = QUESTIONS[index]["answer"]
        user_quiz_index[user_id] = index + 1
        return selected == correct
    return False
