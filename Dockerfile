# Используйте официальный базовый образ Python с версией 3.10.12
FROM python:3.10.12-slim

# Установите рабочую директорию внутри контейнера
WORKDIR /app


# Определяем аргументы сборки
ARG API_KEY
ARG CLIENT_CODE
ARG TELEBOT_KEY

# Задаём переменные окружения
ENV API_KEY=${API_KEY} \
    CLIENT_CODE=${CLIENT_CODE} \
    TELEBOT_KEY=${TELEBOT_KEY}

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
    git  # Добавляем установку Git

# Клонируем репозитории
# RUN git clone https://github.com/cia76/MarketPy.git
# RUN git clone https://github.com/cia76/FinamPy.git
# RUN git clone https://github.com/cia76/BackTraderFinam.git
ENV PYTHONPATH="/app"

# Скопируйте файл зависимостей в рабочую директорию
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы проекта в рабочую директорию
COPY . .

# Задайте команду, которая будет выполняться при запуске контейнера
CMD ["python", "/app/BackTraderFinam/Examples/TeleBotSber.py"]
