# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
COPY app.py /app
COPY sentiment_model.py /app
COPY config.py /app
COPY api_utils.py /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define command to run app
CMD ["python", "app.py"]
