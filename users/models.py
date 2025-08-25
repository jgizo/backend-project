from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLES = [
        ('admin', 'Admin'), 
        ('user', 'User'), 
        ('guest', 'Guest'),
        ('mod', 'Moderator')
    ]

    role = models.CharField(max_length=9, choices=ROLES, default='user')
