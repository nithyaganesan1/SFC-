FROM python:3.8

WORKDIR /code

RUN apt-get update
RUN pip install scapy
RUN apt install -y libpcap0.8
RUN pip install python-socketio

COPY firewallrules.json .
COPY firewall.py .
COPY firewall_PF.py .
COPY plain_PF.py .
COPY dpi.py .
COPY load_balancer.py .
COPY run.py .

ENTRYPOINT ["python3", "run.py"]
