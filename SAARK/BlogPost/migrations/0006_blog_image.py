# Generated by Django 3.0.4 on 2020-05-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0005_blog_uploader'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='Blog.png', upload_to='BlogThumnailimg/'),
        ),
    ]
