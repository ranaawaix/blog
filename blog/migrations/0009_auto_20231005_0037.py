# Generated by Django 3.2.21 on 2023-10-05 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20231005_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
