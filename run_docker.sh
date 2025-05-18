#!/bin/bash

# Перейти в директорію blogger-agent (один рівень вище)
cd ../blogger-agent

# Встановити CONTENT_API_KEY, якщо він переданий як аргумент
if [ ! -z "$1" ]; then
    export CONTENT_API_KEY="$1"
fi

# Вивести інформацію про API ключ
if [ -n "$CONTENT_API_KEY" ]; then
    echo "CONTENT_API_KEY встановлено: $CONTENT_API_KEY"
else
    echo "УВАГА: CONTENT_API_KEY не встановлено"
fi

# Запустити Docker Compose
echo "Запуск Docker Compose з директорії blogger-agent..."
docker compose up --build 