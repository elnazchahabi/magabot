# megabot/modules/vision/voice_to_text.py
import speech_recognition as sr

def convert_voice_to_text(audio_path: str, lang: str = 'fa-IR') -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        return "❌ صدا قابل تشخیص نیست."
    except sr.RequestError as e:
        return f"❌ خطا در ارتباط با Google API: {e}"
