
# Django
from django.contrib import admin

# Models
from .models import Activity, Property,survey

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass

@admin.register(Property)
class ActivityAdmin(admin.ModelAdmin):
    pass
@admin.register(survey)
class ActivityAdmin(admin.ModelAdmin):
    pass

