FROM python:3.11

WORKDIR /app

COPY app/ .

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py", "static/data"]