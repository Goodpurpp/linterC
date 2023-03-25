FROM ubuntu:18.04
COPY ./ /usr/clinter/src
WORKDIR /usr/clinter/src
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN cat packages | xargs apt-get install -y
RUN pip3 install -r requirements.txt
RUN pip3 install pycodestyle
RUN python3 -m pytest --tb=line --cov=. .
RUN find . -iname '*.py' | xargs pycodestyle
