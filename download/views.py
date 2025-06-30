from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "download/index.html")

def download(request):
    return render(request, "download/download.html")

def test_view(request):
    return render(request, "download/test.html")