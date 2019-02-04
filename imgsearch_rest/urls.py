from django.conf import settings
from django.urls import path
from rest_framework import routers

from imgsearch_rest.views import ImgSearchList, ImgSearchDetail

router = routers.DefaultRouter()

urlpatterns = [
    path(settings.IMAGE_SEARCH, ImgSearchList.as_view()),
    path(settings.IMAGE_SEARCH + '<int:pk>/', ImgSearchDetail.as_view()),
]
