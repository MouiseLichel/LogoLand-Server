from django.db import models

# Create your models here.
class ImageSearch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(blank =True, max_length=255)
    results = models.CharField(max_length=255)
