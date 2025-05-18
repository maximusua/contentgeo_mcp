import requests
import json
import os
import sys
from typing import Dict, List, Optional, Any, Union
import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get API key from environment variables (optional)
CONTENT_API_KEY = os.environ.get("CONTENT_API_KEY")
if CONTENT_API_KEY:
    logger.info(f"CONTENT_API_KEY found: {CONTENT_API_KEY[:4]}***. API requests will use the key.")
else:
    logger.info("CONTENT_API_KEY not found. API requests will work without a key.")

# Initialize FastMCP server
PORT = int(os.environ.get("MCP_PORT", 8000))
mcp = FastMCP("contentgeo")

@mcp.tool()
def health_check() -> Dict:
    """
    Check server status.
    
    Returns:
        Dictionary with server status information
    """
    try:
        # Check ContentGeo API availability
        url = "https://api.contentgeo.info/?page=landmarks&lat=50.4113658&lon=30.5113545"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        response = requests.get(url)
        response.raise_for_status()
        
        return {
            'status': 'healthy',
            'api_status': 'available',
            'message': 'Server is functioning normally',
            'api_key_present': bool(CONTENT_API_KEY)
        }
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        return {
            'status': 'unhealthy',
            'api_status': 'unavailable',
            'message': str(e),
            'api_key_present': bool(CONTENT_API_KEY)
        }

@mcp.tool()
def landmarkinfo(ids: str = "") -> Dict:
    """
    Get information about a landmark by its ID.
    
    Args:
        ids: Landmark ID
        
    Returns:
        Dictionary with landmark information
    """
    try:
        if not ids:
            raise ValueError("No landmark ID provided")
            
        url = f"https://api.contentgeo.info/?page=landmarkinfo&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting landmark information: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

@mcp.tool()
def landmarks(lat: float = 0, lon: float = 0) -> Dict:
    """
    Get a list of landmarks near the specified coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Dictionary with a list of landmarks
    """
    try:
        if not lat or not lon:
            raise ValueError("Coordinates not provided")
            
        url = f"https://api.contentgeo.info/?page=landmarks&lat={lat}&lon={lon}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting landmarks list: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon}
        }

@mcp.tool()
def restaurants(lat: float = 0, lon: float = 0) -> Dict:
    """
    Get a list of restaurants near the specified coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Dictionary with a list of restaurants
    """
    try:
        if not lat or not lon:
            raise ValueError("Coordinates not provided")
            
        url = f"https://api.contentgeo.info/?page=restaurants&lat={lat}&lon={lon}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting restaurants list: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon}
        }

@mcp.tool()
def restaurantinfo(ids: str = "") -> Dict:
    """
    Get detailed information about a restaurant by its ID.
    
    Args:
        ids: Restaurant ID
        
    Returns:
        Dictionary with detailed restaurant information
    """
    try:
        if not ids:
            raise ValueError("No restaurant ID provided")
            
        url = f"https://api.contentgeo.info/?page=restaurantinfo&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting restaurant information: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

@mcp.tool()
def geo_objects(lat: float = 0, lon: float = 0, distance: Optional[float] = None) -> Dict:
    """
    Get geo objects near the specified coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        distance: Distance in kilometers (optional)
        
    Returns:
        Dictionary with a list of geo objects
    """
    try:
        if not lat or not lon:
            raise ValueError("Coordinates not provided")
            
        url = f"https://api.contentgeo.info/?page=geo_objects&lat={lat}&lon={lon}"
        if distance is not None:
            url += f"&distance={distance}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting geo objects: {str(e)}")
        return {
            "error": str(e),
            "features": [],
            "coordinates": {"lat": lat, "lon": lon, "distance": distance}
        }

@mcp.tool()
def geo_object_info(ids: str = "") -> Dict:
    """
    Get detailed information about a geo object by its ID.
    
    Args:
        ids: Geo object ID
        
    Returns:
        Dictionary with detailed geo object information
    """
    try:
        if not ids:
            raise ValueError("No geo object ID provided")
            
        url = f"https://api.contentgeo.info/?page=geo_object_info&ids={ids}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error getting geo object information: {str(e)}")
        return {
            "error": str(e),
            "ids": ids
        }

@mcp.tool()
def location_search(query: str = "") -> Dict:
    """
    Search for locations by name or query.
    
    Args:
        query: Location name or search query
        
    Returns:
        Dictionary with search results
    """
    try:
        if not query:
            raise ValueError("No search query provided")
            
        url = f"https://api.contentgeo.info/?page=location_search&query={query}"
        if CONTENT_API_KEY:
            url += f"&api_key={CONTENT_API_KEY}"
            
        logger.info(f"Request to ContentGeo API: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error searching locations: {str(e)}")
        return {
            "error": str(e),
            "query": query,
            "results": []
        }

# Create a WSGI app for the server
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="ContentGeo MCP Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a simple status endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "ContentGeo MCP Server is running"}

# Create an MCP endpoint
@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint():
    return {"status": "ok", "message": "This is the MCP endpoint"}

if __name__ == "__main__":
    import uvicorn
    HOST = os.environ.get("MCP_HOST", "0.0.0.0")
    logger.info(f"Starting server on {HOST}:{PORT}...")
    uvicorn.run(app, host=HOST, port=PORT) 