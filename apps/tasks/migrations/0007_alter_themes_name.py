# Generated by Django 4.2.1 on 2023-05-26 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themes',
            name='name',
            field=models.CharField(max_length=155, unique=True),
        ),
    ]
