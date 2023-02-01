FROM python:3.10.9-slim

# Enviromental Variables
ENV DJANGOFOLDER /djangocode

# Install helpers
COPY ./bins/ /usr/bin/
RUN chmod +x /usr/bin/*

# Prepare Django folder
RUN mkdir /djangocode
WORKDIR /djangocode

# Upgrade pip
RUN pip install --upgrade pip

# Install django and auxiliaries
COPY requirements/ /djangocode/requirements/
RUN pip install -r /djangocode/requirements/development.txt
