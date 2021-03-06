from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

loctype = (
    ('tourist','tourist'),
    ('resteraunt','resteraunts'),
)

# Create your models here.

class Locations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    locationtype = models.CharField(choices=loctype, max_length=60, null=True)
    youtubevideo = models.URLField(null=True, blank=True)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(blank=False, null=True, upload_to="donationprofiles")
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    timeopen = models.TimeField(auto_now=False,null=True, blank=True)
    timeclose = models.TimeField(auto_now=False, null=True,blank=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    verified = models.BooleanField(default=False)
    FOMO = models.FloatField(default=100)


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.pk})


class CommentsField(models.Model):
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='location')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    comment = models.CharField(max_length=400)
    rating = models.IntegerField()
    
    def __str__(self):
        return str(self.location)
    