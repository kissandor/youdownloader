FROM python:3.13-bullseye

ENV PYTHONUNBUFFERED=1

# Szükséges rendszercsomagok (git, libgl rembg-hez, ffmpeg yt_dlp-hez)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár
WORKDIR /downloader

# Követelmények telepítése
COPY requirements.txt /downloader/
RUN pip install --no-cache-dir -r requirements.txt

# Teljes projekt másolása
COPY . /downloader/

# Django fejlesztői szerver indítása
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
