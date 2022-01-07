# django
from django.urls import path, include

# Django Rest FrameWork
from rest_framework.routers import DefaultRouter

# Routers
from .router import router

urlpatterns = [
    path('',include(router.urls))
]
