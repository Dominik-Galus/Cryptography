FROM python:3.11.2

WORKDIR /app

COPY examples/server_1/server_1.py pyproject.toml ./
COPY cryptography ./cryptography

RUN pip install .