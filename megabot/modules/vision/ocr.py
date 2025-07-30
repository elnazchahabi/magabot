# megabot/modules/vision/ocr.py
import pytesseract
from PIL import Image

def extract_text_from_image(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng+fas')
        return text.strip()
    except Exception as e:
        return f"❌ خطا در OCR: {e}"
