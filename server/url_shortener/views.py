from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View
from .models import ShortURL
import random
from django.contrib.auth import logout
import string
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from url_shortener.forms import RegisterForm
from django.http import HttpRequest
from url_shortener.services.url_shortener import URLShortenerService
from url_shortener.forms import ShortenURLForm


class ShortenUrl(View):
    form_class = ShortenURLForm
    template_name = 'url_shortener/index.html'

    @method_decorator(login_required(login_url='url_shortener:login'))
    def get(self, request: HttpRequest):
        user = request.user
        user_urls = ShortURL.objects.filter(owner=user)
        base_url = self.get_base_url(request)

        context: dict[str, str | object] = {'user_urls': user_urls,
                                            'base': base_url}

        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            messages.error(request, 'URL inválida.')
            return redirect('url_shortener:shorten-url')

        user = request.user
        target_url = request.POST.get('long_url')

        shortener_service = URLShortenerService(user, target_url)
        slug = shortener_service.create_short_url()
        print('slug:', slug)

        base_url = self.get_base_url(request)

        # AO INVES DE PEGAR AS URLS E OS DADOS SIMPLESMENTE REDIRECIONAR PRO GET
        user_urls = ShortURL.objects.filter(owner=user)

        context = {'user_urls': user_urls,
                   'base': base_url,
                   'shortened_url': f'{base_url['full']}s/{slug}'}

        return render(request,  self.template_name, context)

    def get_base_url(self, request: HttpRequest):
        scheme = request.scheme
        host = request.get_host()

        url = {'full': f'{scheme}://{host}/',
               'short': f'{host}/'}
        return url


def redirect_view(request: HttpRequest, slug: str):
    url = get_object_or_404(ShortURL, slug=slug)
    return redirect(url.target_url)


class Login(View):

    def get(self, request: HttpRequest):
        form = AuthenticationForm(request)
        context = {'form': form}

        return render(
            request,
            'url_shortener/login.html',
            context,
        )

    def post(self, request: HttpRequest):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('url_shortener:shorten-url')

        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('url_shortener:login')


class SingUp(View):

    def get(self, request: HttpRequest):
        form = RegisterForm
        created_account = False
        context = {
            'form': form,
            'created_account': created_account,
        }

        return render(
            request,
            'url_shortener/singup.html',
            context,
        )

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        context: dict[str, RegisterForm] = {'form': form}
        if form.is_valid():
            user = form.save()

            created_account = True
            context['created_account'] = created_account

        return render(
            request,
            'url_shortener/singup.html',
            context,
        )


class Logout(View):

    @method_decorator(login_required(login_url='url_shortener:login'))
    def get(self, request: HttpRequest):
        logout(request)
        return redirect('url_shortener:login')
