from flask import Flask, url_for, session
from flask import render_template, redirect, abort
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def normalize_twitter_userinfo(client, data):
    # make twitter account data into UserInfo format
    params = {
        'sub': data['id_str'],
        'name': data['name'],
        'email': data.get('email'),
        'locale': data.get('lang'),
        'picture': data.get('profile_image_url_https'),
        'preferred_username': data.get('screen_name'),
    }
    username = params['preferred_username']
    if username:
        params['profile'] = 'https://twitter.com/{}'.format(username)
    return params


oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    userinfo_endpoint='account/verify_credentials.json?include_email=true&skip_status=true',
    userinfo_compliance_fix=normalize_twitter_userinfo,
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)

oauth.register(
        name='facebook',
        access_token_url = 'https://graph.facebook.com/oauth/access_token',
        access_token_params = None,
        authorize_url = 'https://www.facebook.com/dialog/oauth',
        authorize_params = None,
        api_base_url = 'https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )



@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login/<name>')
def login(name):
    client = oauth.create_client(name)
    if not client:
        abort(404)

    redirect_uri = url_for('auth', name=name, _external=True)
    return client.authorize_redirect(redirect_uri)


@app.route('/auth/<name>')
def auth(name):
    client = oauth.create_client(name)
    if not client:
        abort(404)
    token = client.authorize_access_token()
    if 'id_token' in token:
        user = client.parse_id_token(token)
    elif name == "facebook":
        resp = oauth.facebook.get(
    'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
        user = resp.json()
    else:
        user = client.userinfo()
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
