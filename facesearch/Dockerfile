FROM python:3.7

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
RUN python3 image_download.py 芸能人 && python3 train.py

EXPOSE 8080

CMD ["python", "server.py"]

