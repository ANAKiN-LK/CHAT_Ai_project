FROM python:3.12-slim

WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set UV to use system Python only (don't download new Python)
ENV UV_PYTHON_PREFERENCE=only-system

# Install dependencies using pyproject.toml
COPY pyproject.toml .
RUN uv sync --no-dev --no-install-project

# Copy application
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]