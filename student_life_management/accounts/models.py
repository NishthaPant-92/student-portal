from django.db import models
from django.db import models
from django.contrib.auth.models import User

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    screen_time = models.FloatField()
    study_time = models.FloatField()
    stress_level = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


# Create your models here.
