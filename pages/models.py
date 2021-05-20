from django.db import models

# Create your models here.

class Chat(models.Model):
  author_of_message = models.TextField(null=True)
  message = models.TextField()