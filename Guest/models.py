from django.db import models
from Organizer.models import *
# Create your models here.
class organiser(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True)

class ParticipateUser(models.Model):
    user=models.CharField(max_length=50)
    events=models.ForeignKey(Event,on_delete=models.CASCADE)
    rooms=models.TextField(max_length=50,default="")
    new_rooms = models.TextField(max_length=50, default="")
    is_ignored = models.BooleanField(default=False)

class ParticipatePrivateUser(models.Model):
    user=models.CharField(max_length=50)
    events=models.ForeignKey(PrivateEvent,on_delete=models.CASCADE)
    rooms=models.TextField(max_length=50,default="")
    new_rooms = models.TextField(max_length=50, default="")
    is_ignored = models.BooleanField(default=False)
    code=models.ForeignKey(PrivateCodes,on_delete=models.CASCADE)