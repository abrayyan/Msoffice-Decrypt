FROM ubuntu:16.04
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3 \
    python3-dev \
    python3-pip && \
    pip3 install msoffcrypto-tool
WORKDIR /