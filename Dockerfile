FROM python:3.10-slim

WORKDIR /app

# Install uv for faster package installation
RUN pip install uv

# Install dependencies using uv
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "contentgeo_server.py"] 