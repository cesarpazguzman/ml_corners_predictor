FROM ubuntu:bionic
LABEL maintainer="cesar-paz"

USER root
WORKDIR /home/root

#Initial configuration
RUN apt-get update -y && apt install bash-completion && \
      apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget nano sudo curl unzip libjpeg-dev zlib1g-dev libbz2-dev libsqlite3-dev liblzma-dev

RUN printf '%s\n' "source /etc/profile.d/bash_completion.sh" >> ~/.bashrc


#Install Python3.7
RUN wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz && tar zxvf Python-3.7.11.tgz && cd Python-3.7.11 && ./configure --prefix=/home/root/opt/python3.7.11 && make && make install

RUN ln -s /home/root/opt/python3.7.11/bin/python3 /usr/local/bin/python && ln -s /home/root/opt/python3.7.11/bin/pip3 /usr/local/bin/pip


#Install MySQL-Server
RUN apt-get install -y mysql-server


#Create new user for the system
RUN useradd -rm -d /home/cesar -s /bin/bash -g root -G sudo -u 1001 cesar && echo 'cesar:secret' | chpasswd


#Install Java
RUN apt-get install -y openjdk-8-jdk && apt-get clean
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME


#Install Liquibase
RUN wget https://github.com/liquibase/liquibase/releases/download/v4.5.0/liquibase-4.5.0.tar.gz && gunzip liquibase-4.5.0.tar.gz && \
	mkdir /usr/local/liquibase && tar -xf liquibase-4.5.0.tar -C /usr/local/liquibase && chmod +x /usr/local/liquibase/liquibase
ENV PATH $PATH:/usr/local/liquibase
RUN apt install -y maven


#Install Airflow


#Install Jupyter
RUN pip install jupyter
EXPOSE 8888

#Install google-chrome & chromedriver
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
RUN bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
RUN apt -y update && apt -y install google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/95.0.4638.54/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && \
	mv chromedriver /usr/bin/chromedriver && chown root:root /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver

ENV PYTHONIOENCODING=utf-8

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install dataprep

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]