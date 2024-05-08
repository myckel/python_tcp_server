# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV PYTHONPATH=/app

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3097 available to the world outside this container
EXPOSE 3097

# Run main.py when the container launches
CMD ["python", "-u", "-m", "main"]
