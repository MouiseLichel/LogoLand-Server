from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from image_retrieval.search import search
from imgsearch.models import ImageSearch, Result
from imgsearch_rest.serializers import ImgSearchSerializer
from utils.ImageUtils import base64ToOpenCV


class ImgSearchList(APIView):

    def post(self, request, format=None):
        # Get User-Agent
        client = request.META.get('HTTP_USER_AGENT')
        # Get Base URL
        base_url = request.build_absolute_uri('/')

        # Get Image
        image = base64ToOpenCV(request.data['image'])
        results = search(image)

        image_search = ImageSearch(client=client)
        image_search.save()

        for r in results:
            result = Result(image_url=base_url + r['image_url'], score=r['score'], image_search=image_search)
            result.save()

        response = Response(status=status.HTTP_201_CREATED)
        # Add 'Location' header
        response['Location'] = request.build_absolute_uri(str(image_search.id)+'/')

        return response

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImgSearchDetail(APIView):
    """
    Retrieve or update a ImageSearch instance.
    """

    def get_object(self, pk):
        try:
            return ImageSearch.objects.get(pk=pk)
        except ImageSearch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image_search = self.get_object(pk)
        serializer = ImgSearchSerializer(image_search)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image_search = self.get_object(pk)
        validated_urls = request.data['validated_urls']
        results = Result.objects.filter(image_search=image_search)
        for result in results:
            if result.image_url in validated_urls:
                result.positive_feedback = True
            else:
                result.positive_feedback = False
            result.save()

        image_search = self.get_object(pk)
        serializer = ImgSearchSerializer(image_search)
        return Response(serializer.data)
