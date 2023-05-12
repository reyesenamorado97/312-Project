FROM python:3.8.2

#RUN apt-get update

#Set the home directory to /root
ENV HOME /root

#cd into the home directory
WORKDIR /root

#Copy all the app files into the image
COPY . .

#Download dependecies
RUN pip3 install -r requirements.txt

#Allow  port 5000 to be accesed
#from outside the container
EXPOSE 5000
EXPOSE 27017

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

#Run the app
CMD /wait && python3 -u app.py