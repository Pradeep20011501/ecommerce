# Generated by Django 4.1.5 on 2023-03-16 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]