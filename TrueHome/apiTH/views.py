# Django
from django.shortcuts import render

# Dajngo-rest.framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as status_rest
from rest_framework import viewsets
#Serializers
from apiTH import serializers, models

class ActivityView(viewsets.ViewSet):
    def list(self, request):
        return Response()