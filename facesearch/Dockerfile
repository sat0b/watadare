FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY image_download.py /app
COPY train.py /app
COPY server.py /app
COPY templates /app
COPY static /app

RUN python3 image_download.py 芸能人
RUN python3 train.py

EXPOSE 8080

CMD ["python", "server.py"]

