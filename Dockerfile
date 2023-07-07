FROM python:3.11-slim

ENV PYTHONUBBUFFREF 1
ENV PATH "/root/.local/bin:$PATH"
ENV PYTHONPATH "/"

RUN apt update -y \
    && apt install curl -y \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && apt remove curl -y

COPY ./poetry.lock /
COPY ./pyproject.toml /
COPY ./app /app
WORKDIR /app
RUN poetry install