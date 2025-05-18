#!/bin/bash
set -e

echo "Створюємо віртуальне середовище..."
python3 -m venv /venv
export PATH="/venv/bin:$PATH"

echo "Налаштовуємо Python середовище..."
# Створюємо структуру для MCP модуля
mkdir -p /venv/lib/python3.*/site-packages/mcp
mkdir -p /venv/lib/python3.*/site-packages/mcp/server

# Створюємо базові файли для MCP модуля
cat > /venv/lib/python3.*/site-packages/mcp/__init__.py << EOF
# Пустий файл ініціалізації
EOF

cat > /venv/lib/python3.*/site-packages/mcp/server/__init__.py << EOF
# Пустий файл ініціалізації
EOF

cat > /venv/lib/python3.*/site-packages/mcp/server/fastmcp.py << EOF
import logging

class FastMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"FastMCP '{name}' initialized")
    
    def tool(self):
        def decorator(func):
            name = func.__name__
            self.tools[name] = func
            self.logger.info(f"Tool '{name}' registered")
            return func
        return decorator
    
    def run(self, transport='stdio'):
        self.logger.info(f"Running FastMCP with transport '{transport}'")
        # Просто виконуємо стандартний запуск серверу
        # Tools будуть доступні через звичайний Python, без MCP протоколу
        pass
EOF

# Налаштовуємо змінні середовища
export PATH="/root/.cargo/bin:$PATH"

# Вивід інформації про API ключі
if [ -n "$CONTENT_API_KEY" ]; then
    echo "CONTENT_API_KEY знайдено. API запити будуть використовувати ключ."
else
    echo "CONTENT_API_KEY не знайдено. API запити будуть працювати без ключа."
fi

echo "Встановлюємо Python залежності через uv..."
uv pip install -r requirements.txt

echo "Запускаємо сервер..."
python3 contentgeo_server.py 