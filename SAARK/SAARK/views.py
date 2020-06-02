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
from BlogPost.models import Blog

def home(request):
    context = {
        'Blogslist': Blog.objects.filter(Q(ReadyToShow=True)).order_by('-created')
    }
    return render(request, 'home.html', context)

def Search(request):
    if request.method == 'POST':    
        query = request.POST.get('q')
        context = {
            'blogs': Blog.objects.filter(Q(ReadyToShow=True) ,( Q(Blogtiltle__icontains=query) |Q(Discription__icontains=query) )).order_by('-created'),
            'searched':query
        }
        return render(request, 'search/searchresult.html', context)
    return render(request, 'search/searchresult.html')