FROM python:3.7.7-slim-buster

WORKDIR /messervice
COPY requestments.txt /messervice

RUN apt-get update \
    && apt install -y libpq-dev \
    && apt install -y gcc \
	&& pip install --no-cache-dir -r requestments.txt

EXPOSE 5000
#CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD ["python", "app_main.py"]

# docker run -d --name messervice -v /opt/messervice:/messervice -p 5000:5000  messervice
