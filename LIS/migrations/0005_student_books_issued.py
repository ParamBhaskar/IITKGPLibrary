# Generated by Django 4.1.7 on 2023-04-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIS', '0004_reservedbook_remove_issuedbook_student_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='books_issued',
            field=models.TextField(blank=True, default=None),
        ),
    ]
