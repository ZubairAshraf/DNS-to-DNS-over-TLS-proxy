FROM python:2.7
RUN apt-get install openssl
WORKDIR /usr/local/bin
COPY myserver.py .
CMD ["python","myserver.py"]
