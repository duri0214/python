
from django.db import models


class Customer(models.Model):
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    name_kana = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    birthday = models.DateField()

    def __str__(self):
        return self.name
