# Generated by Django 3.0.4 on 2020-05-24 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0014_blog_readytoshow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='UpBlog',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
    ]