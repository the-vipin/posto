"""SAARK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from Bloggers.views import (
    BloggerCreate,
    BloggerView,
    BloggersubscribersToggle,
    subscribedBloggerlist,
)
from BlogPost.views import (
    BlogCreate,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('users.urls')),
    path('DashBoard/', include('Bloggers.urls')),
    path('createblogger/', BloggerCreate.as_view(), name="createblogger"),
    path('Blogger/<slug:slug>', BloggerView.as_view(), name='viewblogger'),
    path('Blogger/<slug:slug>/subscribe', BloggersubscribersToggle.as_view(), name='bloggersubscribetoggle'),
    path('createBlog/<slug:slug>', BlogCreate.as_view(), name="createBlog"),
    path('Reading=', include('BlogPost.urls')),
    path('Subscribed', subscribedBloggerlist.as_view(), name='subscribedbloggers'),
    path('search', views.Search , name='search'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

