from django.db import models


class Deployment(models.Model):
    name = models.CharField(unique=True, max_length=255)
    email = models.CharField(null=False, max_length=255)
    target = models.TextField(null=True, blank=True)
