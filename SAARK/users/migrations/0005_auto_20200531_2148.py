# Generated by Django 3.0.4 on 2020-05-31 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_connetions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connetions',
            name='Phone',
            field=models.IntegerField(blank=True, help_text='enter Number with country code(+91 for india)', null=True),
        ),
    ]
