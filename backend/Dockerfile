FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app/ ./app/

# Copy tests
COPY backend/tests/ ./tests/

# Copy frontend files
COPY frontend/ ./frontend/

# Initialize database and start server
CMD python -c "from app.database import init_db; init_db()" && uvicorn app.main:app --host 0.0.0.0 --port 8000

EXPOSE 8000

