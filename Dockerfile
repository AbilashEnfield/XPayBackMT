# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

RUN apt-get update && \
    apt-get install -y --no-install-recommends g++
RUN pip install --upgrade pip
RUN pip install -U setuptools pip

RUN pip install fastapi[all] fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-multipart pymongo motor

COPY . /code/

EXPOSE 8000
EXPOSE 5432

