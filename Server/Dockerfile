FROM ubuntu:bionic
LABEL maintainer="cesar-paz"

USER root
WORKDIR /home/root

#Initial configuration
RUN apt-get update -y && apt install bash-completion && \
      apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget nano sudo curl

RUN printf '%s\n' "source /etc/profile.d/bash_completion.sh" >> ~/.bashrc


#Install Python3.6 and pip3
RUN apt-get -y install python3-pip && cp /usr/bin/python3 /usr/bin/python && cp /usr/bin/pip3 /usr/bin/pip


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


COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]