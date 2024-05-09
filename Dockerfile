# Используйте официальный базовый образ Python с версией 3.11.8-slim
FROM python:3.11.8-slim

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Определяем аргументы сборки
ARG API_KEY
ARG CLIENT_CODE
ARG TELEBOT_KEY

# Задаём переменные окружения
ENV API_KEY=${API_KEY} \
    CLIENT_CODE=${CLIENT_CODE} \
    TELEBOT_KEY=${TELEBOT_KEY} \
    PATH="/usr/local/bin:${PATH}" \
    PYTHONPATH="/app"

# Установите необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    gcc \
    python3-dev \
    python3-apt \
    libdbus-1-dev \
    libgirepository1.0-dev \
    mc \
    nano \
    git \
    procps

# Скопируйте файл зависимостей в рабочую директорию
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы проекта в рабочую директорию
COPY . .

# Задайте команду, которая будет выполняться при запуске контейнера
CMD ["python", "/app/BackTraderFinam/Examples/TeleBotSber.py"]
