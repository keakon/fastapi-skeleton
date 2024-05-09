FROM python:slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
