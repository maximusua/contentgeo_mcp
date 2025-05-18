# ContentGeo MCP Server

MCP сервер для роботи з ContentGeo API.

## Встановлення

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python contentgeo_server.py
```

## Docker

```bash
docker build -t contentgeo-mcp .
docker run -p 8000:8000 contentgeo-mcp
```

## API Методи

### landmarkinfo

Отримання інформації про визначну пам'ятку за її ID.

```python
GET /landmarkinfo?ids=716927
```

### landmarks

Отримання списку визначних пам'яток поблизу вказаних координат.

```python
GET /landmarks?lat=50.4113658&lon=30.5113545
``` 