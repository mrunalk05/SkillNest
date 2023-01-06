from django.db import models

# Create your models here.

class Employ(models.Model):
    skillex= models.IntegerField()
    skilllevel= models.CharField(max_length=100)
    project= models.TextField()


