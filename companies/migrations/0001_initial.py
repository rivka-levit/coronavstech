# Generated by Django 5.1.2 on 2024-10-14 15:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('Layoffs', 'Layoffs'), ('Hiring Freeze', 'Hiring Freeze'), ('Hiring', 'Hiring')], default='Hiring', max_length=30)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('app_link', models.URLField(blank=True)),
                ('notes', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]
