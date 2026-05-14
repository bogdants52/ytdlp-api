FROM python:3.11-slim
RUN pip install flask youtube-transcript-api==0.6.2
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
