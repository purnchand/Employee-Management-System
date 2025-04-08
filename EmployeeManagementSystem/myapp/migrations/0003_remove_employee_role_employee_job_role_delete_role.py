# Generated by Django 5.1.3 on 2025-04-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_employee_email_alter_employee_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='role',
        ),
        migrations.AddField(
            model_name='employee',
            name='job_role',
            field=models.CharField(default='Not Assigned', max_length=100),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
