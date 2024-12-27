from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    company_name = models.TextField()
    description = models.TextField()
    number_of_employees = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.company_name