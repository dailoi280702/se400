FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .

CMD ["python", "app.py"]
