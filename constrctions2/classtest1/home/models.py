from django.db import models


# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=100,null=f)


class Employee(models.Model):
    first_name=models.CharField(max_length=100,null=False)
    Last_name=models.CharField(max_length=100)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE)
    salary=models.IntegerField(default=0)
    bouns=models.IntegerField(default=0)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    phone=models.IntegerField(default=0)
    hiry_date=models.DateField()
    
