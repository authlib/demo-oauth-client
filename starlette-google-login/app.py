import json
from starlette.config import Config
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth

app = Starlette(debug=True)
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
async def homepage(request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.route('/login')
async def login(request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
    return RedirectResponse(url='/')


@app.route('/logout')
async def logout(request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
