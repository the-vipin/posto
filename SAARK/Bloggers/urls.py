from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from users import views
from .views import (
    BloggerDashboard,
    UpdateBlogger,
    DeleteBlogger,
)


urlpatterns = [
    path('<slug:slug>',BloggerDashboard.as_view(), name='dashboard'),
    path('<slug:slug>/Update', UpdateBlogger.as_view(), name='updateblogger'),
    path('<slug:slug>/Delete', DeleteBlogger.as_view(), name='deleteblogger'),
]