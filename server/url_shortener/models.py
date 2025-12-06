from django.db import models
from django.contrib.auth.models import User


class ShortURL(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='urls')
    slug = models.CharField(max_length=64, unique=True, db_index=True)
    target_url = models.URLField(max_length=2000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_clicks = models.PositiveIntegerField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)


class Click(models.Model):
    short = models.ForeignKey(
        ShortURL, related_name='clicks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    # opcional: preencher via GeoIP
    country = models.CharField(max_length=64, null=True, blank=True)
