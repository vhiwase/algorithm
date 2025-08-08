# Stage 1: Build Stage
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY src/ /app/src

# Run tests
RUN python3 -m unittest discover -s src

# Stage 2: Production Stage
FROM python:3.11-slim-bookworm

# Set the locale to C.UTF-8 to ensure full UTF-8 support.
ENV LANG C.UTF-8

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /usr/local

# Copy application code
COPY src/ /app/src

# Set environment for production
ENV FLASK_CONFIG production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main_app.app:create_app('production')"]
