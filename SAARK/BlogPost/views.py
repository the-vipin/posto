from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView ,DetailView, CreateView, UpdateView, DeleteView, RedirectView
from itertools import chain
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from .models import Blog
from Bloggers.models import Blogger
import urllib.request
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
class Bloglist(ListView):
    model = Blog

class Blogview(DetailView):
    model = Blog
    template_name =  'blogs/blogtemp.html' 

def blogview(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {
        'object': blog,
        'TITLE': blog.Blogtiltle
    }
    return render(request, '%s' % blog.UpBlog , context)
    
class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    template_name =  'Bloggers/BloggerCreationForm.html'
    login_url = 'login'
    fields = ['Blogtiltle','Authors','image','Discription','uploadfile']
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        instances = form.save(commit=False)
        instances.Uploader = self.request.user
        slug = self.kwargs.get("slug")
        instances.BloggerAc = get_object_or_404(Blogger, slug=slug)
        directory =  instances.BloggerAc.BloggerName + '/' + instances.Blogtiltle
        os.mkdir(os.path.join(BASE_DIR, 'templates/bloggersbox/%s' % directory))
        os.mkdir(os.path.join(BASE_DIR, 'static/bloggersbox/%s' % directory ))
        f = open('templates/bloggersbox/%s/%s.html' % (directory, instances.Blogtiltle) ,'wb') 
        f.close()
        instances.UpBlog = 'bloggersbox/%s/%s.html' % (directory, instances.Blogtiltle)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(BlogCreate, self).get_context_data(**kwargs)
        context['TITLE'] = 'create blogpost'
        return context


class UpdateBlog(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Blog
    template_name =  'Bloggers/BloggerCreationForm.html'
    login_url = 'login'
    fields = ['Blogtiltle','Authors','image','Discription']
    success_url = '/'
    
    def form_valid(self, form):
        instances = form.save(commit=False)
        return super().form_valid(form)
    
    def test_func(self):
        Blog = self.get_object()
        if self.request.user == Blog.Uploader:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(UpdateBlog, self).get_context_data(**kwargs)
        context['TITLE'] = 'edit blog details'
        return context

class DeleteBlog(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Blog
    template_name =  'blog/Deleteblog.html'
    login_url = 'login'
    success_url = '/'

    def test_func(self):
        Blog = self.get_object()
        if self.request.user == Blog.Uploader:
            return True
        return False

class BlogPostlikeToggle(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        url_ = blog.get_blogview_url()
        user = self.request.user
        if user.is_authenticated:
            if user in blog.likes.all():
                blog.likes.remove(user)
            else:
                blog.likes.add(user)
                if user in blog.Dislikes.all():
                    blog.Dislikes.remove(user)
        return url_

class BlogPostDislikeToggle(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        url_ = blog.get_blogview_url()
        user = self.request.user
        if user.is_authenticated:
            if user in blog.Dislikes.all():
                blog.Dislikes.remove(user)
            else:
                blog.Dislikes.add(user)
                if user in blog.likes.all():
                    blog.likes.remove(user)
        return url_

class LikedBlogpost(LoginRequiredMixin, ListView):
    model = Blog 
    template_name = 'blogs/userlikedblogs.html'
    context_object_name = 'blogs'
    login_url = 'login'

    def get_queryset(self):
        result = super(LikedBlogpost, self).get_queryset()
        query = self.request.user
        if query:    
            result = Blog.objects.filter(
                Q(likes=query) )
        else:
            result = None
        return result