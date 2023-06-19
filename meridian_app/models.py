# Create your models here.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Last updated: on Wednesday Apr 12 16:03 2022

@author: Ethan Masters

Purpose: Model

Python Version: Python 3.9.13 (main, Aug 25 2022, 18:29:29) 

"""

from django.db import models
from django.contrib.auth.models import User
from django import forms

class ClockIn(models.Model):
    STATUS_CHOICES = [
        ('IN', 'Clocked In'),
        ('OUT', 'Clocked Out'),
        ('BREAK', 'On Meal Break'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='OUT')
    location = models.CharField(max_length=255, blank=True)
    job_notes = models.TextField(blank=True)
    job_costs = models.TextField(blank=True)
    
    def time_punches(self):
        return f"Clock In: {self.time}, Clock Out: {self.clock_out_time}, Meal Break: {self.meal_break_time}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)