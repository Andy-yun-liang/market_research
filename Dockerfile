
#Today is 2025-02-11
#This is my first dockerfile that i am going to be writing by hand.
#This container is a webscraper that scrapes from various shoppify ecommerce store

#1. We need to use python as our base image because the webscraper is in python
FROM python:3.11

#We need to set a working directory insider our scrapy container
WORKDIR /app

#Copy requirements.txt and install dependencies first as it will help with caching.
#Because containers are built layer by layer, we dont have to rebuild as often if we 
#copy and build requirements first as to copying our code base first
COPY requirements.txt /app/

#Install requirements.txt
RUN pip install -r requirements.txt

#Copy the rest of the source code to the container's app directory
COPY . /app/

#Starts running the scraping bot but if i comment it out, we are in interactive mode
#CMD ["scrapy","crawl","shopify_spider"]

