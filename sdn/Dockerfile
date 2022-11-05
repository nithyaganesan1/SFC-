FROM python:3.8

WORKDIR /code

RUN apt-get update

COPY graph.txt . 
COPY sfc.txt .
COPY antColonyOptimization.py .
COPY controller.py .

CMD ["python3", "controller.py"]