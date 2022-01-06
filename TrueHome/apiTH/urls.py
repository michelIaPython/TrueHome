# django
from django.urls import path, include

# Views
from apiTH import viewsets

# Django Rest FrameWork
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('newproperty',viewsets.NewPropertyViewSet, basename='newproperty')

urlpatterns = [
    path('newactivity',views.addNewActivitytesView.as_view(),name='newactivity'),
    path('',include(router.urls))
]
