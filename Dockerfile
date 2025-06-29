FROM python:3.13-bullseye

ENV PYTHONUNBUFFERED=1

# Szükséges rendszercsomagok (git, libgl rembg-hez, stb.)
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /downloader

COPY requirements.txt /downloader/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /downloader/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
