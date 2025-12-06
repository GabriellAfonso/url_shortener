
from django.contrib import admin
from django.urls import path, include
from url_shortener.views import redirect_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('url_shortener.urls')),
    path('s/<str:short_url>/', redirect_view, name='redirect_view'),

]
