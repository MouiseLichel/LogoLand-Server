from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import render
from media.models import Image
from imgsearch.models import ImageSearch
from imgsearch_rest.serializers import ImageSerializer, ImgSearchSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.settings import settings


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
        base_url = request.build_absolute_uri('/')
        print(base_url)
        serializer = ImgSearchSerializer(data=request.data, context={'client':client,'base_url':base_url})
        if serializer.is_valid():
            obj = serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response['Location'] = request.build_absolute_uri(str(obj.id))
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("errors:%s" % serializer.errors)


class ImgSearchDetail(generics.RetrieveAPIView):
    queryset = ImageSearch.objects.all()
    serializer_class = ImgSearchSerializer
