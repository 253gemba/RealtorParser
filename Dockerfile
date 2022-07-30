FROM python:3

RUN apt update
RUN apt install tesseract-ocr -y

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
