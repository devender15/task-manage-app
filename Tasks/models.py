from django.db import models


# Create your models here

class STATUS_OPTIONS(models.TextChoices): 
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    PENDING = 'PENDING'
    HALF_COMPLETED = 'HALF_COMPLETED'
    DONE = 'DONE'
    OVERDUE = 'OVERDUE'

class Task(models.Model):
    name = models.CharField(max_length=100)
    userId = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS.choices, null=True)
    due_date = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return self.name