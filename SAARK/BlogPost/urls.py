from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from users import views
from .views import (
    Blogview,
    UpdateBlog,
    DeleteBlog,
    BlogPostlikeToggle,
    BlogPostDislikeToggle,
    LikedBlogpost,
)
from . import views
urlpatterns = [
    #path('<slug:slug>', Blogview.as_view(), name='BlogPostview'),
    path('<slug:slug>', views.blogview, name='BlogPostview'),
    path('<slug:slug>/Update', UpdateBlog.as_view(), name='updateblog'),
    path('<slug:slug>/Delete', DeleteBlog.as_view(), name='deleteblog'),
    path('<slug:slug>/like', BlogPostlikeToggle.as_view(), name='likeblogpost'),
    path('<slug:slug>/Dislike', BlogPostDislikeToggle.as_view(), name='dislikeblogpost'),
    
]