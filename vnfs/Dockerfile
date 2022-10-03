FROM python:3.8

WORKDIR /code

RUN apt-get update
RUN pip install scapy
RUN apt install -y libpcap0.8
RUN pip install python-socketio

COPY firewall_PF.py .
COPY plain_PF.py .
COPY dpi.py .

ENTRYPOINT ["python3", "plain_PF.py"]
ENTRYPOINT ["python3", "firewall_PF.py"]
ENTRYPOINT ["python3", "dpi.py"]
