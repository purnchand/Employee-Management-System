from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    job_role = models.CharField(max_length=100)
    salary = models.FloatField()
    phone = models.BigIntegerField(unique=True) 
    location = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.full_name}"
