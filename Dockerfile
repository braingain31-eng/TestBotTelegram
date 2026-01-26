FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GUNICORN_CMD_ARGS "--workers=2 --threads=4 --timeout=120 --keep-alive=75"

CMD ["sh", "-c", "gunicorn $GUNICORN_CMD_ARGS -b 0.0.0.0:8080 main:app"]