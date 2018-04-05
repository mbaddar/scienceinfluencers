FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install locales

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -qq wget unzip build-essential cmake gcc libcunit1-dev libudev-dev


ADD . /code
WORKDIR /code
#RUN pip install --no-cache-dir numpy scipy pandas matplotlib 
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 5000