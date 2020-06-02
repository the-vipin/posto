from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
from .models import Blogger
from BlogPost.models import Blog
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
class Bloggerlist(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Blogger

class subscribedBloggerlist(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Blogger
    template_name = 'Bloggers/listofSubscribedbloggers.html'

    def get_context_data(self, **kwargs):
        context = super(subscribedBloggerlist, self).get_context_data(**kwargs)
        context['bloggers'] = Blogger.objects.all()
        return context

class BloggerDashboard(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Blogger
    template_name = 'dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(BloggerDashboard, self).get_context_data(**kwargs)
        Blogger = self.get_object()
        context['Members'] = User.objects.all()
        context['Blogslist'] = Blog.objects.filter(Q(BloggerAc=Blogger))
        context['TITLE'] = 'dashboard ' + Blogger.BloggerName
        return context
    
    def test_func(self):
        Blogger = self.get_object()
        if self.request.user in Blogger.Members.all():
            return True
        elif self.request.user in Blogger.Founder:
            return True
        return False

class BloggerView(DetailView):
    model = Blogger
    template_name = 'Bloggers/blogger.html'

    def get_context_data(self, **kwargs):
        context = super(BloggerView, self).get_context_data(**kwargs)
        Blogger = self.get_object()
        #context['Members'] = User.objects.all()
        context['Blogslist'] = Blog.objects.filter(Q(BloggerAc=Blogger),Q(ReadyToShow=True)).order_by('-created')
        context['TITLE'] = Blogger.BloggerName
        return context
    
class BloggerCreate(LoginRequiredMixin, CreateView):
    model = Blogger
    template_name =  'Bloggers/BloggerCreationForm.html'
    login_url = 'login'
    fields = ['image','BloggerName','About','Members']
    success_url = '/'

    def form_valid(self, form):
        instances = form.save(commit=False)
        instances.Founder = self.request.user
        directory =  instances.BloggerName
        os.mkdir(os.path.join(BASE_DIR, 'templates/bloggersbox/%s' % directory ))
        os.mkdir(os.path.join(BASE_DIR, 'static/bloggersbox/%s' % directory ))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(BloggerCreate, self).get_context_data(**kwargs)
        context['TITLE'] = 'Blogger creation form'
        return context

class UpdateBlogger(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Blogger
    template_name =  'Bloggers/BloggerCreationForm.html'
    login_url = 'login'
    fields = ['image','BloggerName','About','Members']
    success_url = '/'

    def form_valid(self, form):
        instances = form.save(commit=False)
        instances.Founder = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        Blogger = self.get_object()
        if self.request.user in Blogger.Members.all():
            return True
        elif self.request.user in Blogger.Founder:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(UpdateBlogger, self).get_context_data(**kwargs)
        context['TITLE'] = 'Update blogger details'
        return context
class DeleteBlogger(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Blogger
    template_name =  'Bloggers/DeleteBlogger.html'
    login_url = 'login'
    success_url = '/'

    def test_func(self):
        Blogger = self.get_object()
        if self.request.user == Blogger.Founder:
            return True
        return False

class BloggersubscribersToggle(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blogger, slug=slug)
        url_ = blog.get_bloggerview_url()
        user = self.request.user
        if user.is_authenticated:
            if user in blog.subscribers.all():
                blog.subscribers.remove(user)
            else:
                blog.subscribers.add(user)
        return url_