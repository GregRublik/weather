# Используйте официальный образ Python 3.12.4 как базовый
FROM python:3.12.4-slim

# Установите рабочий каталог
WORKDIR /app

#RUN #apt-get update --fix-missing && \
#    apt-get install -y \
#    build-essential \
#    libpq-dev && \
#    rm -rf /var/lib/apt/lists/*

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы приложения в контейнер
COPY . .

# Откройте порт, на котором будет работать Flask
EXPOSE 5000

# Установите переменную окружения для Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Команда для запуска Flask-приложения
CMD ["flask", "run"]