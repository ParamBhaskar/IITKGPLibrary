# Generated by Django 4.1.7 on 2023-04-08 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIS', '0005_alter_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservedbook',
            name='availability',
            field=models.BooleanField(default=False),
        ),
    ]
