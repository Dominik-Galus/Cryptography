FROM python:3.11.2

WORKDIR /app

COPY examples/client_1/client_1.py pyproject.toml ./
COPY cryptography ./cryptography

RUN pip install .