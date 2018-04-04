#FROM python:3.6-alpine
FROM alpine:3.4
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install numpy scipy pandas matplotlib
ADD . /code
WORKDIR /code
#RUN pip install --no-cache-dir numpy scipy pandas matplotlib 
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 5000