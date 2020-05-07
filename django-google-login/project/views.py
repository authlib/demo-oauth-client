import json
from django.urls import reverse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.google.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.google.authorize_access_token(request)
    user = oauth.google.parse_id_token(request, token)
    request.session['user'] = user
    return redirect('/')


def logout(request):
    request.session.pop('user', None)
    return redirect('/')
