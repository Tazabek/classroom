# Generated by Django 4.2.1 on 2023-05-20 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cources', '0009_alter_courcestream_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='courcestream',
            name='is_theme',
            field=models.BooleanField(default=False),
        ),
    ]
