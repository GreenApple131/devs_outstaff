from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class EntriesStatistics(models.Model):
    week_number = models.PositiveIntegerField(null=True)
    amount_of_entries = models.PositiveIntegerField(null=True)
    total_distance = models.FloatField(null=True)
    total_duration = models.DurationField()
    weekly_average_speed = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.week_number}"
    
    def get_distance_in_km(self):
        return self.total_distance/1000
    
    def get_duration_in_seconds(self):
        return self.total_duration.total_seconds()
    
    def get_weekly_average_speed(self):
        hours = self.get_duration_in_seconds()/60/60
        res = self.get_distance_in_km()/hours
        return "%.1f" % res


class Entries(models.Model):
    date = models.DateTimeField(default=datetime.now)
    week_number = models.PositiveIntegerField(null=True)
    distance = models.FloatField(null=False)
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def get_absolute_url(self):
        return f"/entrie/{self.user.username}/{self.id}"
    
    def get_absolute_delete_url(self):
        return f"/report/entrie/{self.id}/delete"

    def get_distance_in_km(self):
        return self.distance/1000

    def get_duration_in_seconds(self):
        return self.duration.total_seconds()
    
    def get_average_speed(self):
        hours = self.get_duration_in_seconds()/60/60
        res = self.get_distance_in_km()/hours
        return "%.1f" % res
