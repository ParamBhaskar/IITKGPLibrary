# Generated by Django 4.1.7 on 2023-04-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIS', '0003_reservedbook_author_reservedbook_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clerk',
            name='insti_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
