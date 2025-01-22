from django.db import models

# Create your models here.
class Department(models.Model):
    dept_no = models.CharField(max_length=100)

    def __str__(self):
        return str(self.dept_no)


class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary = models.FloatField()
    bonus = models.FloatField()
    phone = models.IntegerField() 
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    dept_no = models.ForeignKey('Department', on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default="")
    hire_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
