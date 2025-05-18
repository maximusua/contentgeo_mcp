import requests
import json
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging
from urllib.parse import urlparse, parse_qs

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentGeoServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.base_url = "https://api.contentgeo.info"
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Обробка GET запитів"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path.strip('/')
            query_params = parse_qs(parsed_url.query)
            
            logger.info(f"Отримано запит: {self.path}")
            
            if path == 'landmarkinfo':
                response = self.landmarkinfo(query_params)
            elif path == 'landmarks':
                response = self.landmarks(query_params)
            elif path == 'restaurants':
                response = self.get_restaurants(query_params)
            elif path == 'restaurantinfo':
                response = self.get_restaurant_info(query_params)
            elif path == 'geo_objects':
                response = self.get_geo_objects(query_params)
            elif path == 'geo_object_info':
                response = self.get_geo_object_info(query_params)
            else:
                response = {'error': 'Невідомий endpoint'}
                self.send_error(404)
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Помилка при обробці запиту: {str(e)}")
            self.send_error(500, str(e))
    
    def landmarkinfo(self, params):
        """
        Отримання інформації про визначну пам'ятку за її ID.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник з інформацією про визначну пам'ятку
        """
        try:
            landmark_id = params.get('id', [''])[0]
            if not landmark_id:
                raise ValueError("Не вказано ID пам'ятки")
                
            url = f"{self.base_url}/?page=landmarkinfo&id={landmark_id}"
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні інформації про пам'ятку: {str(e)}")
            raise
            
    def landmarks(self, params):
        """
        Отримання списку визначних пам'яток поблизу вказаних координат.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник зі списком визначних пам'яток
        """
        try:
            lat = params.get('lat', [''])[0]
            lon = params.get('lon', [''])[0]
            
            if not lat or not lon:
                raise ValueError("Не вказано координати")
                
            url = f"{self.base_url}/?page=landmarks&lat={lat}&lon={lon}"
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні списку пам'яток: {str(e)}")
            raise

    def get_restaurants(self, params):
        """
        Отримання списку ресторанів поблизу вказаних координат.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник зі списком ресторанів
        """
        try:
            lat = params.get('lat', [''])[0]
            lon = params.get('lon', [''])[0]
            
            if not lat or not lon:
                raise ValueError("Не вказано координати")
                
            url = f"{self.base_url}/?page=restaurants&lat={lat}&lon={lon}"
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні списку ресторанів: {str(e)}")
            raise

    def get_restaurant_info(self, params):
        """
        Отримання детальної інформації про ресторан за його ID.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник з детальною інформацією про ресторан
        """
        try:
            restaurant_id = params.get('ids', [''])[0]
            if not restaurant_id:
                raise ValueError("Не вказано ID ресторану")
                
            url = f"{self.base_url}/?page=restaurantinfo&ids={restaurant_id}"
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні інформації про ресторан: {str(e)}")
            raise

    def get_geo_objects(self, params):
        """
        Отримання геооб'єктів поблизу вказаних координат.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник зі списком геооб'єктів
        """
        try:
            lat = params.get('lat', [''])[0]
            lon = params.get('lon', [''])[0]
            distance = params.get('distance', [''])[0]
            
            if not lat or not lon:
                raise ValueError("Не вказано координати")
                
            url = f"{self.base_url}/?page=geo_objects&lat={lat}&lon={lon}"
            if distance:
                url += f"&distance={distance}"
                
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні геооб'єктів: {str(e)}")
            raise

    def get_geo_object_info(self, params):
        """
        Отримання детальної інформації про геооб'єкт за його ID.
        
        Args:
            params: Словник з параметрами запиту
            
        Returns:
            Словник з детальною інформацією про геооб'єкт
        """
        try:
            object_id = params.get('ids', [''])[0]
            if not object_id:
                raise ValueError("Не вказано ID геооб'єкту")
                
            url = f"{self.base_url}/?page=geo_object_info&ids={object_id}"
            logger.info(f"Запит до ContentGeo API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Помилка при отриманні інформації про геооб'єкт: {str(e)}")
            raise

def run_server(port: int = 8000):
    """Запуск сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContentGeoServer)
    logger.info(f"Сервер запущено на порту {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server() 