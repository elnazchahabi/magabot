# megabot/handlers/ai_handler.py
from aiogram import Router, types, F
from aiogram.types import Message
from megabot.modules.ai.chatgpt import ask_chatgpt
from megabot.modules.ai.translate import translate_text
from megabot.modules.ai.summarizer import summarize_text
from megabot.modules.vision.ocr import extract_text_from_image
from megabot.modules.vision.voice_to_text import convert_voice_to_text
import os

router = Router()

@router.message(F.text.startswith('/ask'))
async def handle_chatgpt(message: Message):
    prompt = message.text.replace('/ask', '').strip()
    if not prompt:
        await message.answer("✏️ لطفا سوال خود را وارد کنید.")
        return
    reply = await ask_chatgpt(prompt)
    await message.answer(reply)

@router.message(F.text.startswith('/translate'))
async def handle_translate(message: Message):
    text = message.text.replace('/translate', '').strip()
    translated = translate_text(text, dest_lang='en')
    await message.answer(translated)

@router.message(F.text.startswith('/summarize'))
async def handle_summarize(message: Message):
    text = message.text.replace('/summarize', '').strip()
    summary = summarize_text(text)
    await message.answer(summary)

@router.message(F.photo)
async def handle_ocr(message: Message):
    photo = message.photo[-1]
    path = f"temp/{photo.file_unique_id}.jpg"
    await photo.download(destination_file=path)
    text = extract_text_from_image(path)
    os.remove(path)
    await message.answer(text)

@router.message(F.voice)
async def handle_voice(message: Message):
    voice = message.voice
    path = f"temp/{voice.file_unique_id}.ogg"
    await voice.download(destination_file=path)
    text = convert_voice_to_text(path)
    os.remove(path)
    await message.answer(text)
