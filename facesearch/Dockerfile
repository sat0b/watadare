FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY image_download.py /app
COPY batch.py /app
COPY app.py /app
COPY templates /app
COPY static /app

RUN python3 image_download.py 芸能人
RUN python3 batch.py

EXPOSE 8080

CMD ["python", "app.py"]

