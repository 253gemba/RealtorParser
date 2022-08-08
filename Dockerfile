FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install tesseract-ocr -y


RUN mkdir -p /home/app
RUN mkdir -p /home/app/app/staticfiles
WORKDIR /home/app/app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]