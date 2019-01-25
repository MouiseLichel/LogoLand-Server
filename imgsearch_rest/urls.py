from django.conf.urls import url, include
from rest_framework import  routers
from imgsearch_rest.views import ImageList

router = routers.DefaultRouter()
router.register('images', ImageList, 'images')

urlpatterns = [
    url(r'^',include(router.urls))
]