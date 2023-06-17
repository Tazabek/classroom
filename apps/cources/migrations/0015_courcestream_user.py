# Generated by Django 4.2.1 on 2023-05-25 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cources', '0014_cources_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='courcestream',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stream', to=settings.AUTH_USER_MODEL),
        ),
    ]