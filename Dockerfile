FROM debian:stretch-slim
LABEL MAINTAINER "Chandrapal <bnchandrapal@protonmail.com>"

RUN cd /home \
    && apt-get update \
    && apt-get install -y git python python-pip nmap exiftool \
    && git clone --branch v0.2.3-dev https://github.com/aancw/Belati.git \
    && cd Belati \
    && git submodule update --init --recursive --remote \
    && pip install --upgrade --force-reinstall -r requirements.txt \
    && echo 'alias belati="python /home/Belati/Belati.py"' >> ~/.bashrc

WORKDIR /home/Belati

EXPOSE 8000