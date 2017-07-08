FROM python:3
EXPOSE 80
RUN pip3 install flask
RUN mkdir -p /usr/src
COPY *.py /usr/src
WORKDIR /usr/src
CMD ["python", "flask-test.py"]

