import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    return render(request, "download/index.html")

def download(request):
    return render(request, "download/download.html")


def check_status(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', filename)
    is_ready = os.path.exists(file_path)
    return JsonResponse({'ready': is_ready})