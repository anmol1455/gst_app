FROM python:3.9.6-alpine

WORKDIR /gst-flask-app

ADD . /gst-flask-app
RUN apk add build-base
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","run.py"]
