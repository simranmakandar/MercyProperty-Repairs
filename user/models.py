from django.db import models
from django.contrib.auth.models import AbstractUser

class ExtUser(AbstractUser):
    ROLE_CHOICES = [
        ('MANAGER', 'manager'),
        ('WORKER', 'worker'),
    ]
    contact_no = models.IntegerField(blank=False, default=0000000000, verbose_name = 'Contact number')
    skillset = models.CharField(max_length=50, blank=False, default='')
    user_role = models.CharField(max_length=25, blank=False, choices=ROLE_CHOICES, verbose_name = 'User role')
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return self.username
