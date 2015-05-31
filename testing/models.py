from django.db import models

class Comment(models.Model):
    url = models.URLField()
    text = models.TextField()
