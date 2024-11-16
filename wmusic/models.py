from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class SpotifyUserTokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

class UserWeather(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=100,default="NYC")
    temprature = models.SmallIntegerField(default=25)
    weather_condition = models.CharField(max_length=150)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.location} - {self.timestamp}"