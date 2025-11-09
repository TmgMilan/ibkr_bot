FROM debian:bookworm-slim

#update and upgrade
RUN apt-get update && apt-get upgrade -y

#utilities and the jdk needed
RUN apt-get install -y openjdk-17-jre-headless \
			python3 python3-pip python3.11-venv \
			vim

# the working dir
WORKDIR /app

#copying requirement.txt
COPY requirements.txt

#python dependencies install
RUN pip install --no-cache-dir -r requirements.txt

#copying the python client and running it
COPY ./TWS_API/source/pythonclient /app/pythonclient
RUN python3 /app/pythonclient/setup.py install

#copy the actual python file that gives me the results
COPY bot.py .

#the env file that you will need to create to put in ur credentials named IBKR_ACCOUNT_ID
COPY .env .
