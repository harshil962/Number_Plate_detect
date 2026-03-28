import os
import csv
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import UploadForm
from .detector import detect_plate
from .ocr import get_text


def index(request):
    form = UploadForm()
    return render(request, 'index.html', {'form': form})


def detect_plate_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)

            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            plates = detect_plate(file_path)

            results = []

            for plate in plates:
                texts = get_text(plate)

                for text in texts:
                    results.append(text)
                    save_to_csv(text)

            return render(request, 'result.html', {
                'image_url': fs.url(filename),
                'results': results
            })

    return render(request, 'index.html', {'form': UploadForm()})


def save_to_csv(text):
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([text, datetime.now()])