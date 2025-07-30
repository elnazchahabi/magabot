# megabot/modules/ai/chatgpt.py
import os
import openai
from megabot.config import settings

openai.api_key = settings.openai_api_key

async def ask_chatgpt(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ خطا در ارتباط با ChatGPT: {e}"
