# Generated by Django 3.2 on 2021-05-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_topic_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
