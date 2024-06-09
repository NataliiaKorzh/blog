FROM python:3.12-alpine
LABEL maintainer="n.korzhbalyshyna@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
         --disabled-password \
         --no-create-home \
         django-user

USER django-user

CMD ["python", "article/telegram_bot.py"]
