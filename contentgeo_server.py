import requests
import json
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class ContentGeoServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.base_url = "https://api.contentgeo.info"
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Обробка GET запитів"""
        try:
            # Парсимо URL та параметри
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path.strip('/')
            params = dict(urllib.parse.parse_qsl(parsed_path.query))
            
            # Обробляємо різні ендпоінти
            if path == 'landmarkinfo':
                response = self.landmarkinfo(params.get('ids', ''))
            elif path == 'landmarks':
                response = self.landmarks(
                    float(params.get('lat', 0)),
                    float(params.get('lon', 0))
                )
            else:
                response = {"error": f"Невідомий ендпоінт: {path}"}
            
            # Відправляємо відповідь
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def landmarkinfo(self, ids: str) -> Dict:
        """
        Отримання інформації про визначну пам'ятку за її ID.
        
        Args:
            ids: ID визначної пам'ятки
            
        Returns:
            Словник з інформацією про визначну пам'ятку
        """
        try:
            response = requests.get(f"{self.base_url}/?page=landmarkinfo&ids={ids}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def landmarks(self, lat: float, lon: float) -> Dict:
        """
        Отримання списку визначних пам'яток поблизу вказаних координат.
        
        Args:
            lat: Широта
            lon: Довгота
            
        Returns:
            Словник зі списком визначних пам'яток
        """
        try:
            response = requests.get(f"{self.base_url}/?page=landmarks&lat={lat}&lon={lon}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def run_server(port: int = 8000):
    """Запуск сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContentGeoServer)
    print(f"Запуск сервера на порту {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server() 