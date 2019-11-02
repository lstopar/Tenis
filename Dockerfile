FROM python:2

# create app directory
COPY . /src
WORKDIR /src

RUN pip install web.py

# expose port 8080
EXPOSE 8080

# run the command
CMD [ "sh", "run.sh", "config/config-docker.json" ]
