FROM python:3.6

RUN apt-get update -y
RUN apt-get install -y tesseract-ocr &&\
    apt-get install -y tesseract-ocr-eng 

RUN apt-get install imagemagick

COPY ./requirements.txt ./hack_wait.sh /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN sed -i 's/\r//' /hack_wait.sh

ENTRYPOINT [ "/hack_wait.sh" ]