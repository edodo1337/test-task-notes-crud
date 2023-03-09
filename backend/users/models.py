from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.TextField(max_length=100, blank=False)
    birth_date = models.DateField(blank=False)
