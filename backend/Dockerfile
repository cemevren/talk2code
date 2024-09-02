# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY app /backend/app
COPY Pipfile* /backend/

# Install any needed packages specified in requirements.txt
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Make port 8000 available to the world outside this container
EXPOSE 8000

ENV PORT=8000

# Run the application
CMD pipenv run fastapi run --port $PORT