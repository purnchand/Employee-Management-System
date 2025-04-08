# Generated by Django 5.1.3 on 2025-04-05 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('salary', models.FloatField()),
                ('phone', models.IntegerField()),
                ('location', models.CharField(default='', max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.role')),
            ],
        ),
    ]
