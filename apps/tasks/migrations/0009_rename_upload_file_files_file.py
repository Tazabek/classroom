# Generated by Django 4.2.1 on 2023-05-29 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_files'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='upload_file',
            new_name='file',
        ),
    ]
