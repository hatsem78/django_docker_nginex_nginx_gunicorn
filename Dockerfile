FROM python:3.7-alpine

MAINTAINER Hatsembiller App Developer Arg


ENV PAYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install --upgrade pip
RUN pip install flake8

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir -p /opt/services/santander/src
RUN mkdir -p /var/www/html/santander/static/


WORKDIR /opt/services/santander/src

# copy our project code
COPY . /opt/services/santander/src
# expose the port 8005
EXPOSE 8005
RUN adduser -D user
# define the default command to run when starting the container
CMD ['python manage.py', 'collectstatic --noinput' "gunicorn", "--chdir", "app", "--bind", ":8005", "app.wsgi:application"]