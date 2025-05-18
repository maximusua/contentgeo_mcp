import requests
import json
from typing import Dict, List, Optional
from mcp_server import MCPServer

class ContentGeoServer(MCPServer):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.contentgeo.info"
        
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

if __name__ == "__main__":
    server = ContentGeoServer()
    server.run() 