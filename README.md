# ContentGeo MCP Server

A Model Context Protocol (MCP) server for accessing geographical data from ContentGeo API. This server provides endpoints for retrieving landmark information, restaurants, and other geographical data.

## Features

- Retrieves landmarks near specified coordinates
- Gets detailed information about landmarks, restaurants, and geographical objects
- Searches for locations by name
- Works with or without a ContentGeo API key

## Installation

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone this repository
2. (Optional) Set your ContentGeo API key in the `docker-compose.yml` file
3. Run the server using the provided script:

```bash
./run.sh
```

## API Endpoints

- `/health_check` - Check server status
- `/landmarks?lat={lat}&lon={lon}` - Get landmarks near coordinates
- `/landmarkinfo?ids={id}` - Get detailed landmark information
- `/restaurants?lat={lat}&lon={lon}` - Get restaurants near coordinates
- `/restaurantinfo?ids={id}` - Get detailed restaurant information
- `/geo_objects?lat={lat}&lon={lon}&distance={distance}` - Get geographical objects near coordinates
- `/geo_object_info?ids={id}` - Get detailed geographical object information
- `/location_search?query={query}` - Search for locations by name

## Environment Variables

- `CONTENT_API_KEY` - Your ContentGeo API key (optional)
- `MCP_PORT` - Port for the MCP server (default: 8000)

## Built With

- [FastMCP](https://github.com/TabbyML/FastMCP) - Model Context Protocol framework
- Python 3.10
- uv - Fast Python package installer

## License

This project is licensed under the MIT License. 