from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=512)
    nutriments = models.ManyToManyField('Nutriment')

class Nutriment(models.Model):
    name = models.CharField(max_length=256)

class Comment(models.Model):
    url = models.URLField()
    text = models.TextField()
