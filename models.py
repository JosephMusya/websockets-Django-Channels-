from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Values(models.Model):
    integer = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    