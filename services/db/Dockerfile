# Use the official PostgreSQL image as the base image
FROM postgres:13

# Install any additional dependencies needed
RUN apt-get update && apt-get install -y \
    less \
    make \
    vim

RUN ls -l /docker-entrypoint-initdb.d/

# Set the working directory inside the container
WORKDIR /tmp/db

COPY *.sql /docker-entrypoint-initdb.d/



