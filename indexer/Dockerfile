FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . .
COPY ./.env.docker .env

# Install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN pip install httpx

# Command to run your flow
CMD ["python", "workflow.py"]
