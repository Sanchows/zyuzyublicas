FROM python:3.12.2-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROD 1
RUN apt update && apt install sqlite3 -y
WORKDIR /app
ENV PYTHONPATH $PYTHONPATH:$(pwd)
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . ./
RUN sqlite3 technesis.sqlite3 < create_tables.sql || true

ENTRYPOINT ["python", "bot/main.py"]