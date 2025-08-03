# Stage 1: Build Stage
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production Stage
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /usr/local

# Copy application code
COPY src/ /app/src

EXPOSE 5000

CMD ["python3", "src/main_app/app.py"]