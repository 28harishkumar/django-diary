"""diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from user.views import *

urlpatterns = [
    url(r'^admin82/', include(admin.site.urls)),
    url(r'^accounts/login/$',Login.as_view(),name='login'),
    url(r'^accounts/logout/$',Logout.as_view(),name='logout'),
    url(r'^accounts/password_reset/$',PasswordReset.as_view(),name='password_reset'),
    url(r'^accounts/set-password/$',SetPassword.as_view(),name='set_password'),
    url(r'^accounts/password_change/$',PasswordChange.as_view(),name='password_change'),
    url(r'^accounts/register/$',RegisterUser.as_view(),name='register_user'),
    url(r'^accounts/register/success$',RegisterSuccess.as_view(),name='register_success'),
    url(r'^confirm/(?P<confirmation_code>\w{33})/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', confirm),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/', 'template_name':'registration/set_password_form.html',}, name='reset-link'),
    url(r'^', include('diary.urls')),
]
