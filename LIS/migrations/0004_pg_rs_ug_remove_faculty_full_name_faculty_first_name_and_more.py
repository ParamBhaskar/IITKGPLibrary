# Generated by Django 4.1.7 on 2023-03-24 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LIS', '0003_faculty_full_name_student_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('insti_id', models.CharField(blank=True, max_length=10)),
                ('department', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('insti_id', models.CharField(blank=True, max_length=10)),
                ('department', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('insti_id', models.CharField(blank=True, max_length=10)),
                ('department', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='full_name',
        ),
        migrations.AddField(
            model_name='faculty',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='faculty',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]