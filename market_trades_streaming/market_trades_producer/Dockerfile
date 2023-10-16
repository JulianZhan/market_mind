FROM python:3.9-slim

# set the working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# run python script when the container launches
CMD ["python", "market_trades_producer.py"]
