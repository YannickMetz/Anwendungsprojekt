#Create a ubuntu base image with python 3 installed.
FROM python:3.9

#Set the working directory
WORKDIR /

#copy all the files
COPY . .

#Install the dependencies
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip openssh
RUN pip3 install -r requirements.txt
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#Expose the required port
EXPOSE 5000

#Run the command
CMD gunicorn main:app