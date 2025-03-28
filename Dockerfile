FROM python:3.12-slim-bullseye

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# copy application into the container
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# run the application
CMD ["uv", "run", "--no-dev", "fastapi", "run", "app/main.py", "--port", "8000"]