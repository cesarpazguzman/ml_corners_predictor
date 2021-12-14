FROM ubuntu:bionic
LABEL maintainer="cesar-paz"

USER root
WORKDIR /home/root

#Initial configuration
RUN apt-get update -y && apt install bash-completion && \
      apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget nano sudo curl unzip libjpeg-dev zlib1g-dev libbz2-dev libsqlite3-dev liblzma-dev

RUN printf '%s\n' "source /etc/profile.d/bash_completion.sh" >> ~/.bashrc


RUN wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz && tar zxvf Python-3.7.11.tgz && cd Python-3.7.11 && ./configure --prefix=/home/root/opt/python3.7.11 && make && make install

RUN ln -s /home/root/opt/python3.7.11/bin/python3 /usr/local/bin/python && ln -s /home/root/opt/python3.7.11/bin/pip3 /usr/local/bin/pip
RUN pip install dataprep