from rest_framework import serializers

from image_retrieval.search import search
from imgsearch.models import ImageSearch
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
        client = self.context['client']
        base_url = self.context['base_url']

        # Get results
        base64_image = validated_data.pop('image')
        opencv_image = base64ToOpenCV(base64_image)
        results = search(opencv_image)

        # Form image urls
        for result in results:
            result['image_url'] = base_url + result['image_url']

        # Create new 'ImageSearch'
        return ImageSearch.objects.create(
            client=client,
            results=results
        )

    def to_representation(self, obj):
        # get the original representation
        ret = super(ImgSearchSerializer, self).to_representation(obj)

        # remove 'image' field
        ret.pop('image')

        return ret
