#FROM python:3.6-alpine
FROM amancevice/pandas:3.6.4-python3
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 5000