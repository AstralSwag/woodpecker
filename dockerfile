FROM python:3.10-slim

RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    rm -rf /var/lib/apt/lists/*

# Копируем остальные файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменные окружения (если нужно, можно переопределить при запуске контейнера)
ENV TZ=Europe/Moscow
ENV TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ENV TICKET_SYSTEM_TOKEN=your_ticket_system_token
ENV CHAT_ID=your_chat_id

# Запуск приложения
CMD ["python", "woodpecker.py"]