
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f $HEALTHCHECK_URL || exit 1
    