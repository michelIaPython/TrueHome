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

# Serializers
from . import serializers

# Utilities
from .utils import EnablePartianUpdateMixin

class ActivityViewSet(EnablePartianUpdateMixin, viewsets.ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    # Filters 
    filter_backends = [SearchFilter]
    search_fields = ['status','schedule']
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        current_date = date.today()
        past_days = current_date - timedelta(3)
        post_days = current_date + timedelta(2)
        query_date = models.Activity.objects.filter(schedule__gte=past_days,
                                                    schedule__lte=post_days)
        page = self.paginate_queryset(query_date)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query_date, many=True)
        return Response(serializer.data)
    
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = models.Property.objects.all()
    serializer_class = serializers.PropertySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = models.survey.objects.all()
    serializer_class = serializers.surveyDataSerializer