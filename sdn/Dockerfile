FROM python:3.8

WORKDIR /code

RUN apt-get update

COPY controller.py .

CMD ["python3", "controller.py"]