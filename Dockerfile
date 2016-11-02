FROM python

COPY . /opt/tenyks-contrib
WORKDIR /opt/tenyks-contrib

RUN apt-get update -yq && apt-get install -yq build-essential libzmq3-dev
RUN python setup.py install
