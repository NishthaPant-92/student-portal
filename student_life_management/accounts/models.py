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
    # =========================
# EXPENSE TRACKER MODELS
# =========================

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Shopping", "Shopping"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_split = models.BooleanField(default=False)
    total_people = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def split_amount(self):
        if self.is_split and self.total_people > 0:
            return round(self.amount / self.total_people, 2)
        return self.amount

    def __str__(self):
        return self.title

class SplitDetail(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100)
    amount_owed = models.FloatField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person_name} owes ₹{self.amount_owed}"
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    PERIOD_CHOICES = [
        ("monthly", "Monthly"),
        ("weekly", "Weekly"),
        ("daily", "Daily"),
    ]

    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.period} - ₹{self.amount}"

# Create your models here.
