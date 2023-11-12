FROM python:3.10.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy script helpers
COPY ./compose/development/app/runserver /usr/bin/runserver
RUN sed -i 's/\r$//g' /usr/bin/runserver && chmod +x /usr/bin/runserver

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/development.txt

# Prepare Django dir
ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
