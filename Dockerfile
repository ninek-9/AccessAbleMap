# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the Flask application folder into the container at /app
COPY app/ ./app/

# Copy requirements.txt and run.py into the container at /app
COPY requirements.txt run.py ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME AccessAbleMaps

# Run run.py when the container launches
CMD ["python", "run.py", "--host=0.0.0.0", "--port=80"]

