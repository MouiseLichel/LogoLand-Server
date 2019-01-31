from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import render
from media.models import Image
from imgsearch.models import ImageSearch
from imgsearch_rest.serializers import ImageSerializer, ImgSearchSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

# Create your views here.
class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = (IsAdminUser,)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImgSearchList(APIView):

    def post(self, request, format=None):
        client = request.META.get('HTTP_USER_AGENT')
        serializer = ImgSearchSerializer(data=request.data, context=client)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("errors:%s" % serializer.errors)


class ImgSearchDetail(generics.RetrieveAPIView):
    queryset = ImageSearch.objects.all()
    serializer_class = ImgSearchSerializer
