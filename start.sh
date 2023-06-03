#!/bin/bash
docker build -t yandex_market_parser parser
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
