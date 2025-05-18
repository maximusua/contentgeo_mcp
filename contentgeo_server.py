import requests
import json
import os
import sys
from typing import Dict, List, Optional
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Створюємо модуль FastMCP локально
class FastMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"FastMCP '{name}' initialized")
    
    def tool(self):
        def decorator(func):
            self.logger.info(f"Registering tool: {func.__name__}")
            self.tools[func.__name__] = func
            return func
        return decorator
    
    def run(self, transport='stdio'):
        self.logger.info(f"Running FastMCP with transport '{transport}'")
        
        # Запускаємо простий HTTP сервер для обробки MCP запитів
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import urllib.parse
        
        class MCPHTTPHandler(BaseHTTPRequestHandler):
            def _set_headers(self, content_type='application/json'):
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                
            def _send_json_response(self, data):
                self.wfile.write(json.dumps(data).encode())
            
            def do_GET(self):
                try:
                    logger.info(f"Received request: {self.path}")
                    
                    # Parse URL and parameters
                    url_parts = urllib.parse.urlparse(self.path)
                    path = url_parts.path.strip('/')
                    params = dict(urllib.parse.parse_qsl(url_parts.query))
                    
                    # Call appropriate tool
                    if path in self.server.mcp.tools:
                        tool_func = self.server.mcp.tools[path]
                        result = tool_func(**params)
                        self._set_headers()
                        self._send_json_response(result)
                    else:
                        available_tools = list(self.server.mcp.tools.keys())
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self._send_json_response({
                            "error": f"Endpoint not found: {path}",
                            "available_tools": available_tools
                        })
                        
                except Exception as e:
                    logger.error(f"Error processing request: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self._send_json_response({"error": str(e)})
        
        # Start HTTP server
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, MCPHTTPHandler)
        httpd.mcp = self  # Attach MCP instance to server
        logger.info(f"Starting server on port {server_address[1]}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped by user request")
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}")

# Отримуємо API ключ з змінних середовища (опціонально)
CONTENT_API_KEY = os.environ.get("CONTENT_API_KEY")
if CONTENT_API_KEY:
    logger.info(f"CONTENT_API_KEY found: {CONTENT_API_KEY[:4]}***. API requests will use the key.")
else:
    logger.info("CONTENT_API_KEY not found. API requests will work without a key.")

# Ініціалізація FastMCP сервера
mcp = FastMCP("contentgeo")

@mcp.tool()
def health_check() -> Dict:
    """
    Перевірка стану сервера.
    
    Returns:
        Словник з інформацією про стан сервера
    """
    try:
        # Перевіряємо доступність API ContentGeo
        url = "https://api.contentgeo.info/?page=landmarks&lat=50.4113658&lon=30.5113545"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        response = requests.get(url)
        response.raise_for_status()
        
        return {
            'status': 'healthy',
            'api_status': 'available',
            'message': 'Сервер працює нормально',
            'api_key_present': bool(CONTENT_API_KEY)
        }
    except Exception as e:
        logger.error(f"Помилка при перевірці стану: {str(e)}")
        return {
            'status': 'unhealthy',
            'api_status': 'unavailable',
            'message': str(e),
            'api_key_present': bool(CONTENT_API_KEY)
        }

@mcp.tool()
def landmarkinfo(ids="") -> Dict:
    """
    Отримання інформації про визначну пам'ятку за її ID.
    
    Args:
        ids: ID пам'ятки
        
    Returns:
        Словник з інформацією про визначну пам'ятку
    """
    try:
        if not ids:
            raise ValueError("Не вказано ID пам'ятки")
            
        url = f"https://api.contentgeo.info/?page=landmarkinfo&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні інформації про пам'ятку: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

@mcp.tool()
def landmarks(lat=0, lon=0) -> Dict:
    """
    Отримання списку визначних пам'яток поблизу вказаних координат.
    
    Args:
        lat: Широта
        lon: Довгота
        
    Returns:
        Словник зі списком визначних пам'яток
    """
    try:
        lat = float(lat)
        lon = float(lon)
        
        if not lat or not lon:
            raise ValueError("Не вказано координати")
            
        url = f"https://api.contentgeo.info/?page=landmarks&lat={lat}&lon={lon}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні списку пам'яток: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon}
        }

@mcp.tool()
def restaurants(lat=0, lon=0) -> Dict:
    """
    Отримання списку ресторанів поблизу вказаних координат.
    
    Args:
        lat: Широта
        lon: Довгота
        
    Returns:
        Словник зі списком ресторанів
    """
    try:
        lat = float(lat)
        lon = float(lon)
        
        if not lat or not lon:
            raise ValueError("Не вказано координати")
            
        url = f"https://api.contentgeo.info/?page=restaurants&lat={lat}&lon={lon}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні списку ресторанів: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon}
        }

@mcp.tool()
def restaurantinfo(ids="") -> Dict:
    """
    Отримання детальної інформації про ресторан за його ID.
    
    Args:
        ids: ID ресторану
        
    Returns:
        Словник з детальною інформацією про ресторан
    """
    try:
        if not ids:
            raise ValueError("Не вказано ID ресторану")
            
        url = f"https://api.contentgeo.info/?page=restaurantinfo&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні інформації про ресторан: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

@mcp.tool()
def geo_objects(lat=0, lon=0, distance=None) -> Dict:
    """
    Отримання геооб'єктів поблизу вказаних координат.
    
    Args:
        lat: Широта
        lon: Довгота
        distance: Відстань у кілометрах (опціонально)
        
    Returns:
        Словник зі списком геооб'єктів
    """
    try:
        lat = float(lat)
        lon = float(lon)
        distance = float(distance) if distance is not None else None
        
        if not lat or not lon:
            raise ValueError("Не вказано координати")
            
        url = f"https://api.contentgeo.info/?page=geo_objects&lat={lat}&lon={lon}"
        if distance:
            url += f"&distance={distance}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні геооб'єктів: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon, "distance": distance}
        }

@mcp.tool()
def geo_object_info(ids="") -> Dict:
    """
    Отримання детальної інформації про геооб'єкт за його ID.
    
    Args:
        ids: ID геооб'єкту
        
    Returns:
        Словник з детальною інформацією про геооб'єкт
    """
    try:
        if not ids:
            raise ValueError("Не вказано ID геооб'єкту")
            
        url = f"https://api.contentgeo.info/?page=geo_object_info&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Запит до ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Помилка при отриманні інформації про геооб'єкт: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

if __name__ == "__main__":
    # Ініціалізація та запуск сервера
    logger.info("Запуск FastMCP сервера...")
    mcp.run(transport='stdio') 