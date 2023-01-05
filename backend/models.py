from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    is_manager = models.BooleanField('Is manager', default=False)
    is_employee = models.BooleanField('Is employee', default=False)


class domain(models.Model):
    domain_id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    skillName=models.CharField(max_length=20)
    domain=models.CharField(max_length=20)
    

class skill(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    userName=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain_id=models.ForeignKey(domain, null=False, blank=False, on_delete=models.CASCADE)
    years=models.IntegerField()
    skillLevel=models.CharField(max_length=20)
    projectdes=models.TextField()