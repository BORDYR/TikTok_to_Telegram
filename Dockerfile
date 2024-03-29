# set base image (host OS)
FROM python:3.8

RUN apt-get update && apt-get -y install cron

# Create directories
RUN mkdir logs
RUN mkdir videos
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY / .


#RUN cron

# command to run on container start
RUN crontab -l | { cat; echo "0 20 * * * bash -c \"cd /code ;/usr/local/bin/python3 /code/main.py\""; } | crontab -

ENTRYPOINT [ "cron", "-f" ]
