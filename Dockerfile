FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app ./app
COPY data ./data
COPY models ./models
COPY start.sh .

RUN chmod +x start.sh

EXPOSE 10000

CMD ["./start.sh"]
