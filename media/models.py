from django.db import models
import uuid
def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to=scramble_uploaded_filename)