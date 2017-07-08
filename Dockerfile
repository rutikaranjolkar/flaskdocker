FROM ubuntu:latest

# We need some basic Ubuntu tools to begin with
RUN apt-get update
RUN apt-get -y dist-upgrade
RUN apt-get install -y software-properties-common

# Install Java.
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer

# Define JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Install python and related tools
RUN apt-add-repository universe
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y g++ 
RUN apt-get install -y python3-dev

# Actual work starts
EXPOSE 80
RUN pip3 install flask
RUN pip3 install pyathenajdbc
RUN mkdir -p /usr/src
COPY *.py /usr/src
WORKDIR /usr/src
RUN which java
CMD ["python3", "flask-rest-api.py"]

