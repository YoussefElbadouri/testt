FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

