from django.db import models

# Create your models here.
class Geodata(models.Model):
    postcode = models.PositiveIntegerField(default=0,blank=True)
    locality = models.CharField(max_length=100,blank=True)
    state = models.CharField(max_length=10,blank=True)
    lon = models.FloatField(blank=True)
    lat = models.FloatField(blank=True)
    def __str__(self):
        return self.locality