from rest_framework import serializers
from imgsearch.models import ImageSearch
from media.search import search
from drf_extra_fields.fields import Base64ImageField
import base64
from PIL import Image
import io
import numpy
import cv2
from utils.ImageUtils import base64ToOpenCV


class ImgSearchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    client = serializers.CharField(read_only=True)
    image = serializers.CharField(max_length=None)
    results = serializers.CharField(read_only=True)

    class Meta:
        model = ImageSearch
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `ImageSearch` instance, given the validated data.
        """
        # Save User-Agent
        client = self.context

        # Get results
        base64_image = validated_data.pop('image')
        opencv_image = base64ToOpenCV(base64_image)
        results = search(opencv_image)

        # Create new 'ImageSearch'
        return ImageSearch.objects.create(
            client=client,
            results=results
        )

    def to_representation(self, obj):
        # get the original representation
        ret = super(ImgSearchSerializer, self).to_representation(obj)

        # remove 'image' field if mobile request
        ret.pop('image')

        return ret


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'image')
