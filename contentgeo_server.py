import requests
import json
import os
from typing import Dict, List, Optional
import logging
from mcp.server.fastmcp import FastMCP

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отримуємо API ключ з змінних середовища (опціонально)
CONTENT_API_KEY = os.environ.get("CONTENT_API_KEY")
if CONTENT_API_KEY:
    logger.info("CONTENT_API_KEY знайдено. API запити будуть використовувати ключ.")
else:
    logger.info("CONTENT_API_KEY не знайдено. API запити будуть працювати без ключа.")

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
def landmarkinfo(id: str) -> Dict:
    """
    Отримання інформації про визначну пам'ятку за її ID.
    
    Args:
        id: ID пам'ятки
        
    Returns:
        Словник з інформацією про визначну пам'ятку
    """
    try:
        if not id:
            raise ValueError("Не вказано ID пам'ятки")
            
        url = f"https://api.contentgeo.info/?page=landmarkinfo&id={id}"
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
            "id": id
        }

@mcp.tool()
def landmarks(lat: float, lon: float) -> Dict:
    """
    Отримання списку визначних пам'яток поблизу вказаних координат.
    
    Args:
        lat: Широта
        lon: Довгота
        
    Returns:
        Словник зі списком визначних пам'яток
    """
    try:
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
def get_restaurants(lat: float, lon: float) -> Dict:
    """
    Отримання списку ресторанів поблизу вказаних координат.
    
    Args:
        lat: Широта
        lon: Довгота
        
    Returns:
        Словник зі списком ресторанів
    """
    try:
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
def get_restaurant_info(ids: str) -> Dict:
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
def get_geo_objects(lat: float, lon: float, distance: Optional[float] = None) -> Dict:
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
def get_geo_object_info(ids: str) -> Dict:
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