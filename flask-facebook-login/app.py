from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)


app.secret_key = 'myscretkey'
# configuraciones de oauth
oauth = OAuth(app)
facebook = oauth.register(
    name='facebook',
    client_id="",
    client_secret="",
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)


@app.route("/")
def index():
    return 'Example of Facebook and Authlib'


@app.route('/login')
def registro():
    facebook = oauth.create_client('facebook')
    redirect_uri = url_for('authorize', _external=True)
    return facebook.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    facebook = oauth.create_client('facebook')
    token = facebook.authorize_access_token()
    resp = facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    # do something with the token and profile
    print(profile, token)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=4000)
