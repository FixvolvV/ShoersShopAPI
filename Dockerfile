FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install --upgrade pip 'poetry==2.3.2'
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY src .

COPY alembic ./alembic
COPY alembic.ini .

COPY certs.template ./certs.template

CMD ["sh", "-c", "alembic upgrade head && fastapi run shoersshopapi --port 8030 --host 0.0.0.0"]