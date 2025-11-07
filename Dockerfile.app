# Per generar la imatge des del directori del Dockerfile executar
# docker build -t scrapeapp/scrapeapp:latest .

FROM python:3.12

LABEL name="inventoryapp"
LABEL version="1.0"

WORKDIR /app/inventory

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Latest postgres client

RUN apt update && apt install -y \
    wget \
    gnupg \
    lsb-release \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt update && apt install -y \
    postgresql-client-16 \
    && apt-get clean

# Install system dependencies
RUN apt-get update \
  && apt-get -y install apt-utils iputils-ping net-tools gcc\
  && apt-get clean

# Upgrading pip
RUN pip install --upgrade pip

# Install python depedencies
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# Copying all the code
COPY ./ .


EXPOSE 8000

RUN "python manage.py runserver"
# Copiar fichero de arranque de servicios




