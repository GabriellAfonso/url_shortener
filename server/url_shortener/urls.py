from django.urls import path, include
from url_shortener import views
from url_shortener.views import redirect_view


app_name = 'url_shortener'

urlpatterns = [

    path('', views.ShortenUrl.as_view(), name='shorten-url'),
    path('login/', views.Login.as_view(), name='login'),
    path('singup/', views.SingUp.as_view(), name='singup'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('s/<str:slug>/', redirect_view, name='redirect_view'),
]
