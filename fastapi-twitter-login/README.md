# Twitter login demo with FastAPI

First, copy `.env.sample` to `.env`:

    $ cp .env.sample .env

Create your Twitter OAuth Client and fill the client ID and secret
into `.env`, then run:

    $ python app.py

When register your Twitter OAuth Client, remember to put:

    http://127.0.0.1:5000/

into the client redirect uris list.
