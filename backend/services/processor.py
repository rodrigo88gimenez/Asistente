import pytesseract
from PIL import Image


def process_file(path, content_type):
    if "image" in content_type:
        return extract_text_from_image(path)
    else:
        return read_text(path)


def extract_text_from_image(path):
    return pytesseract.image_to_string(Image.open(path))


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""
