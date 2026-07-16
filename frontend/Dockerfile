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
COPY app.py .
COPY chainlit.md .
COPY public/ ./public/

# Expose port
EXPOSE 8080

# Run Chainlit
CMD ["uv", "run", "chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]