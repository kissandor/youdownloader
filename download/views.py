import os
import re
import unicodedata
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import yt_dlp

def sanitize_filename(name, max_length=100):
    # Ékezetek eltávolítása
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Tiltott karakterek kiszűrése
    name = re.sub(r'[^\w\s.-]', '', name)
    # Szóközök helyett _
    name = re.sub(r'\s+', '_', name)
    return name[:max_length]


def download(request):
    return render(request, "download/download.html")


def check_status(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', filename)
    is_ready = os.path.exists(file_path)
    return JsonResponse({'ready': is_ready})


def index(request):
    return render(request, "download/index.html")


def index(request):
    download_url = None
    filename = None
    if request.method == 'POST':
        video_url = request.POST.get('inputUrl')
        # video_format = request.POST.get('radio_format')
        video_format = 'mp4'

        if not video_url:
            return HttpResponse("Nem adtál meg URL-t!", status=400)

        try:
            file_path = download_media(video_url, video_format)
            print("file_path: " + file_path)
            filename = os.path.basename(file_path)
            print("filename: " + filename)
            media_rel_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
            print("media_rel_path: " + media_rel_path)
            download_url = settings.MEDIA_URL + \
                media_rel_path.replace('\\', '/')
            print("download_url: " + download_url)

            url = reverse('download:success')
            print("url: " + url)
            params = urlencode({'file': filename, 'url': download_url})
            print("params: " + params)
            return redirect(f"{url}?{params}")

        except Exception as e:
            return HttpResponse(f"Hiba történt: {str(e)}", status=500)

    return render(request, 'download/index.html')


def success(request):
    filename = request.GET.get('file')
    download_url = request.GET.get('url')

    if not filename or not download_url:
        return HttpResponse("Hiányzó adatok!", status=400)

    return render(request, 'download/download.html', {
        'filename': filename,
        'download_url': download_url,
    })


def download_media(link, download_file_type='m4a'):

    output_path = os.path.join(
        settings.MEDIA_ROOT, 'downloads', download_file_type)
    
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    print("Letöltési mappa:", output_path)
    
    os.makedirs(output_path, exist_ok=True)
    # Alap beállítások (közösek)
    ydl_opts = {
        'outtmpl': f'{output_path}/%(id)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
    }

    # Különbségek hozzáadása
    if download_file_type == 'mp4':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
        success_msg = "Video downloaded successfully as MP4!"
    else:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': download_file_type,
                    'preferredquality': '192',
                }
            ],
        })
        success_msg = f"Audio downloaded successfully as {download_file_type.upper()}!"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info = ydl.extract_info(link, download=True)
            base_filename = ydl.prepare_filename(info).rsplit('.', 1)[0]
            if download_file_type != 'mp4':
                saved_file_path = f"{base_filename}.{download_file_type}"
            else:
                saved_file_path = f"{base_filename}.mp4"
        return saved_file_path
    except Exception as e:
        print(f"Error during download: {e}")
