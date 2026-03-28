import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cascade_path = os.path.join(BASE_DIR, 'models', 'haarcascade_plate.xml')

cascade = cv2.CascadeClassifier(cascade_path)

if cascade.empty():
    print("❌ Cascade not loaded. Check file.")
else:
    print("✅ Cascade loaded")

def detect_plate(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("❌ Image not loaded")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = cascade.detectMultiScale(gray, 1.1, 4)

    return [img[y:y+h, x:x+w] for (x, y, w, h) in plates]