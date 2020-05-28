# Twitter login demo with Starlette

First, copy `.env.sample` to `.env`:

    $ cp .env.sample .env

Create your Twitter OAuth Client and fill the client ID and secret
into `.env`, then run:

    $ python app.py

When registering your Twitter OAuth Client, remember to put:

    http://127.0.0.1:5000/auth

into the "Callback URL" list.
