from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from SAARK.util import unique_slug_generator_for_blogPost
from django.db.models.signals import pre_save
from Bloggers.models import Blogger
import os
from django.urls import reverse
from django.contrib import admin

class Blog(models.Model):
    Blogtiltle = models.CharField(max_length=50)
    Discription = models.CharField(max_length=999 , blank=True, null=True)
    BloggerAc = models.ForeignKey(Blogger,related_name='bloggerAc', on_delete=models.PROTECT)
    Authors = models.ManyToManyField(User, related_name='BlogMembers')
    UpBlog = models.CharField(max_length=999, null=True, blank=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    Uploader = models.ForeignKey(User,related_name='bloguploader', on_delete=models.PROTECT)
    image = models.ImageField(default='Blog.png', upload_to='BlogThumnailimg/' , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='blogpostLikes',blank=True)
    Dislikes = models.ManyToManyField(User, related_name='blogpostdislike',blank=True)
    uploadfile = models.FileField(upload_to='upBlogs/' ,blank=True)
    ReadyToShow = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created','-modified')
    
    def __str__(self):
        return f'{self.Blogtiltle} Blog'
    
    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'slug':self.slug})
    
    def get_blogview_url(self):
        return reverse('BlogPostview',kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,500)
            img.thumbnail(output_size)
            img.save(self.image.path)
        
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_for_blogPost(instance)
    
pre_save.connect(pre_save_receiver, sender = Blog)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('Blogtiltle', 'ReadyToShow')
    
admin.site.register(Blog, BlogAdmin)
    