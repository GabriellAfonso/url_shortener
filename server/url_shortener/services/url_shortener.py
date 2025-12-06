import random
from django.utils.crypto import get_random_string
from url_shortener.models import ShortURL
from django.db import IntegrityError
from django.contrib.auth.models import User


class URLShortenerService:
    def __init__(self, user: User, url: str) -> None:
        self.owner = user
        self.target_url = url

    def create_short_url(self, length=6):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        while True:
            slug = get_random_string(length, allowed_chars=chars)
            print('aa')
            try:
                ShortURL.objects.create(
                    owner=self.owner,
                    target_url=self.target_url,
                    slug=slug
                )
                return slug
            except IntegrityError:
                # colisão: tenta novamente
                continue
