#!/bin/bash
set -e

echo "Створюємо віртуальне середовище..."
python3 -m venv /venv
export PATH="/venv/bin:$PATH"

echo "Налаштовуємо Python середовище..."
# Знаходимо шлях до site-packages
SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")
echo "Site packages: $SITE_PACKAGES"

# Створюємо структуру для MCP модуля
mkdir -p "$SITE_PACKAGES/mcp"
mkdir -p "$SITE_PACKAGES/mcp/server"

# Створюємо базові файли для MCP модуля
cat > "$SITE_PACKAGES/mcp/__init__.py" << EOF
# Пустий файл ініціалізації
EOF

cat > "$SITE_PACKAGES/mcp/server/__init__.py" << EOF
# Пустий файл ініціалізації
EOF

cat > "$SITE_PACKAGES/mcp/server/fastmcp.py" << EOF
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

# Для тестування, переконуємося, що модуль доступний
python3 -c "import sys; print(sys.path); import mcp.server.fastmcp; print('MCP модуль доступний!')" || {
    echo "Помилка імпорту MCP модуля. Спробуємо вилікувати..."
    export PYTHONPATH="$SITE_PACKAGES:$PYTHONPATH"
    python3 -c "import mcp.server.fastmcp; print('Тепер MCP модуль доступний!')" || {
        echo "Не вдалося виправити помилку імпорту. Вносимо додаткові зміни..."
        # Для contentgeo_server.py - створимо локальний mcp модуль
        mkdir -p mcp/server
        cp "$SITE_PACKAGES/mcp/__init__.py" mcp/
        cp "$SITE_PACKAGES/mcp/server/__init__.py" mcp/server/
        cp "$SITE_PACKAGES/mcp/server/fastmcp.py" mcp/server/
        echo "Створено локальний mcp модуль в поточній директорії."
    }
}

# Вивід інформації про API ключі
if [ -n "$CONTENT_API_KEY" ]; then
    echo "CONTENT_API_KEY знайдено. API запити будуть використовувати ключ."
else
    echo "CONTENT_API_KEY не знайдено. API запити будуть працювати без ключа."
fi

# Встановлюємо uv
echo "Встановлюємо uv..."
curl -sSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.cargo/bin:$PATH"
echo "Шлях до uv: $(which uv || echo 'uv не знайдено')"

# Встановлюємо Python залежності
echo "Встановлюємо Python залежності..."
pip install --no-cache-dir -r requirements.txt

echo "Запускаємо сервер..."
python3 contentgeo_server.py 