# Generated by Django 5.1.3 on 2025-04-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_employee_job_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
