FROM python:3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY index_builder.py /app

CMD ["python", "index_builder.py"]
