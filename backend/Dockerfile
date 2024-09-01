# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /backend

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy the current directory contents into the container at /backend
COPY app /backend/app
COPY Pipfile* /backend/
COPY .env /backend/

# Install any needed packages specified in Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV MODULE_NAME="app.main"
ENV VARIABLE_NAME="app"
ENV PORT=80

# Run the application
CMD uvicorn $MODULE_NAME:$VARIABLE_NAME --host 0.0.0.0 --port $PORT