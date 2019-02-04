from django.db import models


# Create your models here.
class ImageSearch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=255)
    image = models.TextField()


class Result(models.Model):
    image_url = models.URLField()
    score = models.FloatField()
    image_search = models.ForeignKey(ImageSearch, related_name='results', on_delete=models.CASCADE)
