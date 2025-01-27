# Generated by Django 5.1.4 on 2025-01-27 15:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_post_community'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
