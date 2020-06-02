from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Bio = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='User_profile/')

    def __str__(self):
        return f'{self.user.username} Userprofile'
    
   # def get_absolute_url(self):
    #    return reverse('user-profile', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super(Userprofile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Connetions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Phone = models.IntegerField(help_text="enter Number with country code(+91 for india)" , blank=True , null=True)
    instagram = models.URLField(max_length=999, blank=True , null=True)
    FaceBook = models.URLField(max_length=999, blank=True , null=True)
    Linkdin = models.URLField(max_length=999, blank=True , null=True)
    YouTube = models.URLField(max_length=999, blank=True , null=True)
    Twitter = models.URLField(max_length=999, blank=True , null=True)
    TikTok = models.URLField(max_length=999, blank=True , null=True)
    Website = models.URLField(max_length=999, blank=True , null=True)
    Blogs = models.URLField(max_length=999, blank=True , null=True)
    YourQuotes = models.URLField(max_length=999, blank=True , null=True)

    def __str__(self):
        return f'{self.user.username} Connetions'
    
