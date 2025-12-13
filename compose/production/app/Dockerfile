# ----- Builder Step -----
FROM python:3.11.14-slim as builder

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY ./requirements/ ./requirements/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements/production.txt

# ----- Final Step -----
FROM python:3.11.14-slim

# Create a directory for the non-root user
RUN mkdir /app

# Create the non-root user
RUN addgroup --system halfuser && adduser --system --group halfuser

# Create all related directories
ENV HOME=/app
ENV APP_HOME=/app/halfquiz

# Create SQLite data directory
RUN mkdir -p $HOME/sqlite-data && chown halfuser:halfuser $HOME/sqlite-data/

# Create necessary Django staticfiles directory
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/media && chown -R halfuser:halfuser $APP_HOME

WORKDIR $APP_HOME

# Install Python dependencies from builder wheels
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy entrypoint.sh
COPY ./compose/production/app/entrypoint.sh $HOME/entrypoint.sh
RUN sed -i 's/\r$//g' $HOME/entrypoint.sh && chmod +x $HOME/entrypoint.sh

# Copy start.sh
COPY ./compose/production/app/start.sh $HOME/start.sh
RUN sed -i 's/\r$//g' $HOME/start.sh && chmod +x $HOME/start.sh

# Copy only the necessary project files (order matters due to cache optimization)
COPY --chown=halfuser:halfuser manage.py $APP_HOME/manage.py
COPY --chown=halfuser:halfuser config/ $APP_HOME/config/
COPY --chown=halfuser:halfuser templates/ $APP_HOME/templates/
COPY --chown=halfuser:halfuser apps/ $APP_HOME/apps/

# Change to the non-root user
USER halfuser

VOLUME ["/app/halfquiz/staticfiles", "/app/halfquiz/media", "/app/sqlite-data"]

ENTRYPOINT ["/app/entrypoint.sh"]

