# Generated by Django 3.2.21 on 2023-10-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_contactus_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]
