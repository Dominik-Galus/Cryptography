FROM python:3.11.2

WORKDIR /app

COPY examples/client_2/client_2.py pyproject.toml ./
COPY cryptography ./cryptography

RUN pip install .