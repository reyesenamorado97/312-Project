version: '3.3'
services:
  mongo:
    image: mongo:4.2.5
    ports:
      - '27018:27017'
  app:
    build: .
    environment:
      WAIT_HOSTS: mongo:27017
    ports:
      - '8080:5000'