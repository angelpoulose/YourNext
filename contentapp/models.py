from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    genres = models.TextField(null=True)
    languages=models.TextField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

class Watched(models.Model):
    title = models.TextField(null = True)
    content = models.TextField(null = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    on_added = models.DateTimeField(auto_now_add=True)

