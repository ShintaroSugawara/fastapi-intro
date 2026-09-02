FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["sh", "-c", "python -m api.migrate_db && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"]