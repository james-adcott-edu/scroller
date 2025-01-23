from django.db import migrations, models
from django.utils.text import slugify

def populate_slug(apps, schema_editor):
    Community = apps.get_model('forum', 'Community')
    for community in Community.objects.all():
        community.slug = slugify(community.name)
        community.save()

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),  # Replace with the actual previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='slug',
            field=models.SlugField(unique=True, max_length=25, null=True, blank=True),
        ),
        migrations.RunPython(populate_slug),
        migrations.AlterField(
            model_name='community',
            name='slug',
            field=models.SlugField(unique=True, max_length=25),
        ),
    ]