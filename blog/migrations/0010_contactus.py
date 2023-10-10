# Generated by Django 3.2.21 on 2023-10-05 12:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20231005_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999999999)])),
                ('message', models.TextField()),
            ],
        ),
    ]
