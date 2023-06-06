FROM python:3.11.3

WORKDIR /telegram_bot

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    pip install --upgrade setuptools \
    pip install -r requirements.txt

COPY . .
