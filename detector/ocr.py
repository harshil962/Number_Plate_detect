import easyocr
import re


reader = easyocr.Reader(['en'], gpu=False)

def fix_indian_plate(text):
    # Expected format: AA00AA0000

    if len(text) >= 10:
        text = list(text)

        # Positions:
        # 0-1: letters
        # 2-3: numbers
        # 4-5: letters
        # 6-9: numbers

        # Fix numbers positions
        for i in [2, 3, 6, 7, 8, 9]:
            if text[i] == 'O': text[i] = '0'
            if text[i] == 'I': text[i] = '1'
            if text[i] == 'L': text[i] = '4'   # 🔥 important fix

        return "".join(text)

    return text


def get_text(image):
    results = reader.readtext(image)

    texts = []
    for (_, text, _) in results:
        clean = re.sub(r'[^A-Z0-9]', '', text.upper())

        clean = fix_indian_plate(clean)

        if len(clean) >= 8:
            texts.append(clean)

    return texts