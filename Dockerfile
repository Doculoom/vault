FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .

RUN uv pip install --no-cache --system -r pyproject.toml

COPY . .

ENV PYTHONPATH=/app
RUN uv run python -m app.utils.build_utils

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
