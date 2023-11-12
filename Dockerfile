# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml ./

RUN ls -la

COPY . .

# Install dependencies
RUN pip3 install setuptools wheel && \
    pip3 install --no-cache-dir .

ENV PYTHONUNBUFFERED=True

CMD nycmesh-calendar-bot