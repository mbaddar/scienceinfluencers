FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y locales python3 python3-pip python3-dev python3-virtualenv fabric \
      libpq-dev libjpeg-dev libxml2-dev libxslt-dev libfreetype6-dev libffi-dev \
      postgresql-client git curl wget
# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Check python version
RUN python --version
# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -qq wget unzip build-essential cmake gcc libcunit1-dev libudev-dev apt-utils 


ADD . /code
WORKDIR /code
#RUN pip install --no-cache-dir numpy scipy pandas matplotlib 
RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 5000