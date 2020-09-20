"""Doraemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.contrib import admin

from Doraemon.settings import GOTO_URL, MEDIA_ROOT, STATIC_ROOT, DEBUG
from Doraemon.view import *

app_name = "Doraemon"

urlpatterns = [
    path('', IndexView.as_view()),
    path("ok/", alive_view),
    path('admin/', admin.site.urls),
    path(GOTO_URL, GoToView.as_view()),
    path('search/', SearchView.as_view()),
    path('sign/', SignView.as_view()),
]

urlpatterns.extend([
    path('auth/password_reset/', AsyncMailPasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
])

if DEBUG:
    urlpatterns.extend([
        re_path('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    ])
