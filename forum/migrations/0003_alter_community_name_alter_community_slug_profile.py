# Generated by Django 5.1.4 on 2025-01-23 15:41

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_community_slug_alter_community_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=25, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_name', message='Community name must be lowercase ASCII letters and underscores only.', regex='^[a-z_]+$'), django.core.validators.MaxLengthValidator(25)]),
        ),
        migrations.AlterField(
            model_name='community',
            name='slug',
            field=models.SlugField(blank=True, max_length=25, unique=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
