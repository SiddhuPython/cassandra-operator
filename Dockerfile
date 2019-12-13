FROM ubuntu:latest

MAINTAINER "sudhakar.donkena@xoriant.com"

RUN apt-get update \
 && apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN apt-get update \
 && apt-get install -y curl 

COPY . /app

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
