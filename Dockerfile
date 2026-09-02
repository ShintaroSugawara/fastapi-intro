FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root

COPY . .

CMD ["sh", "-c", "poetry run python -m api.migrate_db && poetry run uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]