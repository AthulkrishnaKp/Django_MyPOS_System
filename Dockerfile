FROM python:alpine

# Set the working directory in the container
WORKDIR /app
# Install system dependencies, including pkg-config
RUN apk update && \
    apk add python3-dev mariadb-dev build-base
# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

# Grant execute permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

