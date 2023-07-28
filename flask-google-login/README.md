# Google login demo with Flask

You can learn Flask OAuth 2.0 client with this demo.

## Install

Install the required dependencies:

    $ pip install -U Flask Authlib requests

## Config

Create your Google OAuth Client at <https://console.cloud.google.com/apis/credentials>, make sure to add `http://127.0.0.1:5000/auth` into Authorized redirect URIs.

Fill the given client ID and secret into `config.py`.

## Run

Start server with:

    $ export FLASK_APP=app.py
    $ flask run

Then visit:

    http://127.0.0.1:5000/
