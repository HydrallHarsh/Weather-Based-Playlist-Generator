"""
URL configuration for playlist_generator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('get-weather/', views.get_weather, name='get_weather'),
    path('login/' , views.login , name = 'login'),
    path('logout/' , views.logout_view , name = 'logout'),
    path('register/' , views.register , name = 'register'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/user_playlists/', views.user_playlists, name='user_playlists'),
    path('generate_playlists/',views.generate_playlists,name='generate_playlists'),

    
]
