FROM python:3.11

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в /bot
WORKDIR /bot

# Копируем все содержимое текущей директории в /bot в контейнере
COPY . .

# Обновляем pip и устанавливаем зависимости из requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Команда, которая будет выполнена при запуске контейнера
CMD ["python", "main.py"]