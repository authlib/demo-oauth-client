# Flask Oauth with major providers

You can learn Flask OAuth client with this demo.

## Install

Install the required dependencies:

    $ pip install -U Flask Authlib requests

## Config

Google:

Create your Google OAuth Client at <https://console.cloud.google.com/apis/credentials>, make sure to add `http://localhost:5000/google/auth/` into Authorized redirect URIs.

Twitter:
Create your Twitter Oauth 1.0 Client at <https://developer.twitter.com/> by creating a app.
Add `http://localhost:5000/twitter/auth/` into Authorized redirect URIs.

Facebook:
Create your Facebook OAuth Client at <https://developer.facebook.com/>, by creating a app.
Add `http://localhost:5000/facebook/auth/` into Authorized redirect URIs.
## Run

Start server with:

python app.py

Then visit:

    http://localhost:5000/
