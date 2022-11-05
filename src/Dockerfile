FROM python:3.8

WORKDIR /code

RUN apt-get update
RUN pip install scapy
RUN apt install -y libpcap0.8

COPY client_1.py .
COPY client_2.py .
COPY client_3.py .
COPY client_4.py .
COPY client_5.py .
COPY run.py .


CMD ["python3", "run.py"]