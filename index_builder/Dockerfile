FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY batch.py /app

CMD ["python", "batch.py"]
