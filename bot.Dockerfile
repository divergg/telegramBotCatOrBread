FROM python:3.11


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /botFrontend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /botFrontend .

CMD python bot.py