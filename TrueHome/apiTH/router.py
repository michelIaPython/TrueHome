# Django rest FrameWork
from rest_framework import routers

#Api
from apiTH.viewsets import ActivityViewSet, PropertyViewSet, SurveyViewSet


router = routers.DefaultRouter()
router.register('property',PropertyViewSet)
router.register('activity',ActivityViewSet)
router.register('survey',SurveyViewSet, basename="survey")