FROM python:3.13-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "python", "bot.py"]
