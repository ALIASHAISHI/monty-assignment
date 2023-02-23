# Use the official Python image as a parent image
FROM python:3.8-slim-buster

# environment varibles
ENV app_port 5000

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE ${app_port}

# Start the Flask app when the container launches
CMD ["flask", "run"]
