FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg\
    pkg-config \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

CMD ["python", "consumer.py"]