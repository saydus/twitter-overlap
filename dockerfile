FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG STORAGE_URL
ENV STORAGE_URL=$STORAGE_URL



CMD ['python', 'fetchFollowers.py']