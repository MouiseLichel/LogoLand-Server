from rest_framework import serializers
from .models import ImageSearch, Image
from .custom_fields import Base64ImageField
from search_engine.search import Engine

class ImgSearchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    client = serializers.CharField(required=False)
    image = Base64ImageField(max_length=None)
    results = serializers.CharField(read_only=True)

    class Meta:
        model = ImageSearch
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `ImageSearch` instance, given the validated data.
        """
        client = self.context
        results = Engine.search(validated_data['image'])
        return ImageSearch.objects.create(
            client=client,
            results=results
        )

    def to_representation(self, obj):
        # get the original representation
        ret = super(ImgSearchSerializer, self).to_representation(obj)

        # remove 'url' field if mobile request
        ret.pop('image')

        return ret

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk','image')