from django.conf.urls import url, include
from rest_framework import  routers
from imgsearch_rest.views import ImageList , ImageDetail
from django.urls import path

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^',include(router.urls)),
    path('images/', ImageList.as_view()),
    path('images/<int:pk>/', ImageDetail.as_view()),
]