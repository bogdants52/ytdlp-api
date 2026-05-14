FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl unzip && rm -rf /var/lib/apt/lists/*

RUN pip install flask yt-dlp yt-dlp-get-pot

WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
