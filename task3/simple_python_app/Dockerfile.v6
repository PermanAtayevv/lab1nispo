# syntax=docker/dockerfile:1
FROM python:3.14-slim AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip wheel --no-cache-dir -r /tmp/requirements.txt --wheel-dir /wheels

FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,from=builder,source=/wheels,target=/wheels \
    pip install --no-cache-dir --no-index /wheels/*

RUN groupadd --system app \
    && useradd --system --gid app --no-create-home app

WORKDIR /app

COPY --chown=app:app app.py /app/app.py

USER app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
