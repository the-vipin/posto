from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from users import views
from BlogPost.views import (
    LikedBlogpost,
)

urlpatterns = [
    path('', views.profile, name='profile'),
    url(r'signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_account, name='activate'),
    path('update/', views.updateprofile, name='update-profile'),
    path('Liked/', LikedBlogpost.as_view(), name='likedblogs'),
]