FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY image_download.py /app

CMD ["python", "image_download.py"]
