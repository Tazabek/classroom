# Generated by Django 4.2.1 on 2023-05-18 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cources', '0005_courcefeed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourceFeed',
            new_name='CourceStream',
        ),
    ]