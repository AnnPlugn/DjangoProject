FROM python:3.11

# Устанавливаем переменную окружения для буферизации вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app/

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска Django-сервера
CMD ["python", "/app/djangoProjectFirst/manage.py", "runserver", "0.0.0.0:8000"]