# Generated by Django 4.1.7 on 2023-04-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIS', '0006_remove_student_books_issued'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuedbook',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]