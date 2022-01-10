# Python 
from datetime import date, timedelta

# Django
from django.shortcuts import get_object_or_404

# Django Rest FrameWork
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

# Models
from . import models
from django.db.models import Q

# Serializers
from . import serializers

# Utilities
from .utils import EnablePartianUpdateMixin

class ActivityViewSet(EnablePartianUpdateMixin, viewsets.ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    # Filters 
    filter_backends = (SearchFilter, )
    search_fields = ('status', 'schedule')
    
    def get_queryset(self):
        current_date = date.today()
        past_days = current_date - timedelta(4)
        post_days = current_date + timedelta(3)
        query = models.Activity.objects.filter(schedule__gte=past_days,
                                                    schedule__lte=post_days)
        return query
    
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = models.Property.objects.all()
    serializer_class = serializers.PropertySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = models.survey.objects.all()
    serializer_class = serializers.surveyDataSerializer