from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import render
from media.models import Image
from imgsearch_rest.serializers import ImageSerializer, ImgSearchSerializer

# Create your views here.
class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    #permission_classes = (IsAdminUser,)

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer