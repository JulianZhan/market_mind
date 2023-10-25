FROM python:3.9-slim

# set the working directory in the container to /app
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# run the command to start up the api server
CMD ["python", "app.py"]
