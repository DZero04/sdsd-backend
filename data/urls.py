from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('diabetesdata', DiabetesDataViewSet, basename='diabetesdata')
router.register('regiondata', RegionViewSet, basename='regiondata')
urlpatterns = router.urls