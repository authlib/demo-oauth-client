from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)


app.secret_key = 'myscretkey'
# configuraciones de oauth
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id='',
    client_secret='',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route("/")
def index():
    return 'Hello!'


@app.route('/login')
def registro():
    github = oauth.create_client('github')
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    # do something with the token and profile
    print(profile, token)
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
