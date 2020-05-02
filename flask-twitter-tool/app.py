from flask import Flask, url_for, request
from flask import session, render_template, redirect
from authlib.integrations.flask_client import OAuth, OAuthError


app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

oauth = OAuth(app)
oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)


@app.errorhandler(OAuthError)
def handle_error(error):
    return render_template('error.html', error=error)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.twitter.authorize_access_token()
    url = 'account/verify_credentials.json'
    resp = oauth.twitter.get(url, params={'skip_status': True})
    user = resp.json()
    # DON'T DO IT IN PRODUCTION, SAVE INTO DB IN PRODUCTION
    session['token'] = token
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/tweets')
def list_tweets():
    url = 'statuses/user_timeline.json'
    params = {'include_rts': 1, 'count': 200}
    prev_id = request.args.get('prev')
    if prev_id:
        params['max_id'] = prev_id

    resp = oauth.twitter.get(url, params=params)
    tweets = resp.json()
    return render_template('tweets.html', tweets=tweets)
