from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from imgsearch.models import ImageSearch
from imgsearch_rest.serializers import ImgSearchSerializer


class ImgSearchList(APIView):

    def post(self, request, format=None):
        # Get User-Agent
        client = request.META.get('HTTP_USER_AGENT')
        # Get Base URL
        base_url = request.build_absolute_uri('/')

        # Serialize the data
        serializer = ImgSearchSerializer(data=request.data, context={'client': client, 'base_url': base_url})
        if serializer.is_valid():
            obj = serializer.save()
            response = Response(status=status.HTTP_201_CREATED)

            # Add 'Location' header
            response['Location'] = request.build_absolute_uri(str(obj.id))

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImgSearchDetail(generics.RetrieveAPIView):
    queryset = ImageSearch.objects.all()
    serializer_class = ImgSearchSerializer
