FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-get -y install libc-dev --fix-missing
RUN apt-get -y install build-essential
# Add deadsnakes repo with different python versions
# Default version on Ubuntu 20.04 is 3.8
# https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install -y python3.8 python3.8-dev 
RUN apt-get install -y python3-pip

RUN apt-get install -y gcc gfortran musl-dev

RUN python3.8 -m pip install --upgrade pip

# install some dev requirements
COPY requirements-dev.txt /dataflow/requirements.txt
RUN python3.8 -m pip install -r /dataflow/requirements.txt

COPY . /dataflow
WORKDIR /dataflow

# install the semantic machines package to access dataflow helpers
RUN python3.8 -m pip install .

# install our lispress to graph program package
WORKDIR /dataflow/dreamcoder
RUN python3.8 setup.py build
RUN python3.8 -m pip install .