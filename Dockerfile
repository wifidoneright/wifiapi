# don't forget to log in to docker hub
FROM alpine

RUN apk update 
RUN apk upgrade -U -a

RUN apk add uwsgi-python3
RUN apk add python3 py3-pip
#Required to install python library dependencies
RUN apk add openssh
RUN apk add python3-dev
RUN apk add gcc
RUN apk add libc-dev
RUN apk add libffi-dev
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pip setuptools
RUN pip3 install wheel

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip3 install -r requirements.txt

RUN addgroup -S -g 10001 appGrp \
    && adduser -S -D -u 10000 -s /sbin/nologin -h /app -G appGrp app \
    && chown -R 10000:10001 /app

USER 10000:10001

# run command at start
CMD ["uwsgi", "app.ini"]
