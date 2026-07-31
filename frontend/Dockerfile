FROM python:3.12-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_PYTHON_PREFERENCE=only-system
COPY pyproject.toml .
RUN uv sync --no-dev --no-install-project
COPY app.py .
EXPOSE 8080
CMD ["uv", "run", "chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]