# enable python etcd interaction
# /opt/dockernotes creating

FROM quay.io/signalfuse/maestro-base:14.04-0.1.8.1
MAINTAINER David Liu <davidbliu@gmail.com>
ENV DEBIAN_FRONTEND noninteractive

# add python-etcd 
ADD . /opt/dockernotes
WORKDIR /opt/dockernotes/python-etcd

# install python-etcd dependencies
RUN apt-get update
RUN apt-get -y install python-dev
RUN apt-get -y install libffi-dev
RUN apt-get -y install libssl-dev 
RUN python setup.py install

WORKDIR /opt/dockernotes
