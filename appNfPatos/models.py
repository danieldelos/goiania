from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(null=True)
    birthdate = models.DateField(null=True)
    married = models.BooleanField(default=False)