from django.db import models

# Create your models here.
class Event(models.Model):
    code=models.CharField(max_length=50,unique=True)
    rooms=models.IntegerField()
    org=models.ForeignKey("Guest.organiser",on_delete=models.CASCADE)
    status=models.IntegerField(default=0)

class Room(models.Model):
    events=models.ForeignKey(Event,on_delete=models.CASCADE)
    number=models.CharField(max_length=50)
    capacity=models.IntegerField(default=0)
