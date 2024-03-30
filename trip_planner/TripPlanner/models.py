from django.db import models
from django.contrib.auth.models import Group as AuthGroup, Permission

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TripPlan(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Participant(models.Model):
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    activities = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField()
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.activities} - {self.date}"

class Plan(models.Model):
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PlanSelection(models.Model):
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    selected_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trip_plan} - {self.selected_plan}"


class Expenditure(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=50)  

class ExpenditureSplit(models.Model):
    expenditure = models.ForeignKey(Expenditure, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2)
