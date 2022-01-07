# Python 
from datetime import date, timedelta, datetime

# Django
from django.db.models import query
from django.http import request
from django.shortcuts import get_object_or_404

# Django Rest FrameWork
from rest_framework import viewsets
from rest_framework import status
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
        query_date = models.Activity.objects.filter(schedule__gte=past_days , schedule__lte=post_days)
        #query_date = get_object_or_404(models.Activity, schedule__gte=past_days , schedule__lte=post_days)
        #print(query_date)
        #print("CURRENT DAY : ",current_date)
        #print("OLD Date : ",current_date - timedelta(3))
        #print("new Date:")
        #for each_obj in queryset:
        #    print(each_obj.schedule)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = models.Property.objects.all()
    serializer_class = serializers.PropertySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = models.survey.objects.all()
    serializer_class = serializers.surveyDataSerializer