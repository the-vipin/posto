from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from SAARK.util import unique_slug_generator
from django.db.models.signals import pre_save
import os
from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your models here.

class Blogger(models.Model):
    image = models.ImageField(default='team.png', upload_to='Blogger_profile/')
    BloggerName = models.CharField(max_length=50, unique=True)
    Founder = models.ForeignKey(User,related_name='Founders', on_delete=models.PROTECT)
    Members = models.ManyToManyField(User, related_name='bloggerMembers')
    About = models.CharField(max_length=500)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers',blank=True)

    def __str__(self):
        return self.BloggerName
    
    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'slug':self.slug})
    
    def get_bloggerview_url(self):
        return reverse('viewblogger', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        super(Blogger, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(pre_save_receiver, sender = Blogger)



    
    

