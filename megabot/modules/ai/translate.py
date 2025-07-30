# megabot/modules/ai/translate.py
from googletrans import Translator

translator = Translator()

def translate_text(text: str, dest_lang: str = 'en') -> str:
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except Exception as e:
        return f"❌ خطا در ترجمه: {e}"
