# Generated by Django 4.1.7 on 2023-03-31 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LIS', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
