from django.contrib import admin
from django.urls import path, include
from apiTH.router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apiTH.urls')),
]
