# syntax=docker/dockerfile:1

FROM python:3.9
WORKDIR /discordBOT
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python bot.py