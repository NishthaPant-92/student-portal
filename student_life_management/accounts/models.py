from django.db import models
from django.contrib.auth.models import User

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wake_up_time = models.TimeField(null=True, blank=True)
    sleep_time = models.TimeField(null=True, blank=True)
    breakfast_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)

    screen_time = models.FloatField()
    study_time = models.FloatField()

    stress_level = models.CharField(max_length=50)

    date = models.DateField(auto_now_add=True)
    stress_status = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

# Create your models here.
