# Google login demo with Django

You can learn Django OAuth 2.0 client with this demo.

## Install

Install the required dependencies:

    $ pip install -U Django Authlib requests

## Config

Create your Google OAuth Client at <https://console.cloud.google.com/apis/credentials>, make sure to add `http://127.0.0.1:8000/auth/` into Authorized redirect URIs.

Fill the client ID and secret into `project/settings.py`, then run:

    $ python manage.py migrate

## Run

Start server with:

    $ python manage.py runserver

Then visit:

    http://127.0.0.1:8000/
