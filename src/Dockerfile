FROM python:3.12.8-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROD 1
RUN apt update && apt install -y sqlite3 wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt clean

WORKDIR /app
ENV PYTHONPATH $PYTHONPATH:$(pwd)
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . ./
RUN sqlite3 technesis.sqlite3 < create_tables.sql || true

ENTRYPOINT ["python", "bot/main.py"]