# Generated by Django 5.0.6 on 2024-05-30 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]