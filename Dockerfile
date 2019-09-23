FROM python:3.6.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update && apt-get install -y memcached binutils libproj-dev gdal-bin && rm -rf /var/lib/apt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /code/

