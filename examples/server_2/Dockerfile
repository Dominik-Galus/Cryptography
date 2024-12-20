FROM python:3.11.2

WORKDIR /app

COPY examples/server_2/server_2.py pyproject.toml ./
COPY src/cryptography ./src/cryptography

RUN pip install .