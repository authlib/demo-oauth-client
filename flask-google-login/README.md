# Google login demo with Flask

Create your Google OAuth Client and fill the client ID and secret
into `config.py`, then run:

    $ export FLASK_APP=app.py
    $ flask run

When register your Google OAuth Client, remember to put:

    http://127.0.0.1:5000/

into the client redirect uris list.
