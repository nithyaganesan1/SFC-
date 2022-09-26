FROM python:3.8

WORKDIR /code

RUN apt-get update
RUN pip install scapy
RUN apt install -y libpcap0.8

COPY client_1.py .

CMD ["python3", "client_1.py"]