FROM python:3.10-slim-bullseye
WORKDIR /book-management-service
RUN apt update -y && apt upgrade -y
RUN apt install -y curl nano vim git
COPY ./requirements.txt /book-management-service/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /book-management-service/requirements.txt
COPY . /book-management-service/
ARG HOST="0.0.0.0"
ENV APP_HOST=$HOST
ARG PORT=8000
ENV PORT_NUMBER=$PORT
EXPOSE $PORT_NUMBER
ARG DEBUG=False
ENV DEBUG_MODE=$DEBUG
ARG JWT_SECRET_KEY
ARG DB_PATH
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY
ARG POSTGRES_USER
ENV POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD
ARG POSTGRES_HOST
ENV POSTGRES_HOST
ARG POSTGRES_PORT
ENV POSTGRES_PORT
ARG POSTGRES_DB
ENV POSTGRES_DB
ENV DB_PATH=$DB_PATH
CMD python main.py

