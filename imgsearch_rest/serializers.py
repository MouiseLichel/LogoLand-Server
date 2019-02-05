from rest_framework import serializers

from image_retrieval.search import search
from imgsearch.models import ImageSearch, Result
from utils.ImageUtils import base64ToOpenCV


class ResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image_url = serializers.URLField()
    score = serializers.FloatField()
    positive_feedback = serializers.NullBooleanField(required=False)

    class Meta:
        model = Result
        fields = ['id','image_url', 'score','positive_feedback' ]

    def to_representation(self, obj):
        # get the original representation
        ret = super(ResultSerializer, self).to_representation(obj)

        # remove 'id' field
        ret.pop('id')

        return ret


class ImgSearchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    client = serializers.CharField(read_only=True)
    results = ResultSerializer(many=True, read_only=True)

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
            Result(image_url=base_url + result['image_url'], score=result['score'])

        # Create new 'ImageSearch'
        return ImageSearch.objects.create(
            client=client,
            results=results
        )