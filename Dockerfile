FROM python:3.11

# Устанавливаем переменную окружения для буферизации вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /djangoProjectFirst

# Копируем файл зависимостей в контейнер
COPY requirements.txt /djangoProjectFirst/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /djangoProjectFirst/

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000