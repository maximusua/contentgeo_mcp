#!/bin/bash
set -e

echo "Створюємо віртуальне середовище..."
python3 -m venv /venv
export PATH="/venv/bin:$PATH"

# Вивід інформації про API ключі
if [ -n "$CONTENT_API_KEY" ]; then
    echo "CONTENT_API_KEY знайдено: $CONTENT_API_KEY"
    echo "API запити будуть використовувати ключ."
else
    echo "CONTENT_API_KEY не знайдено. API запити будуть працювати без ключа."
fi

# Встановлюємо Python залежності
echo "Встановлюємо Python залежності..."
pip install --no-cache-dir -r requirements.txt

echo "Запускаємо HTTP сервер..."
python3 contentgeo_server.py 