# Generated by Django 3.0.6 on 2020-05-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.TextField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(default='', max_length=2550),
        ),
    ]
