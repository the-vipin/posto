# Generated by Django 3.0.4 on 2020-05-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0008_auto_20200522_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='UpBlog',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]