FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY app.py /app
COPY templates /app/templates
COPY static /app

EXPOSE 8080

CMD ["python", "app.py"]

