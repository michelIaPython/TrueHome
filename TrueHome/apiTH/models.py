from django.db import models

class Property(models.Model):
    """this is the model's property"""
    tittle = models.CharField(max_length=255,blank = False)
    address = models.TextField(blank = False)
    description = models.TextField(blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    disable_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=35, blank=True)
    def __str__(self) -> str:
        return self.tittle

class Activity(models.Model):
    """this is the model's activity"""
    
    tittle = models.CharField(max_length=255,blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35, blank=True)
    schedule = models.DateTimeField(auto_created=True ,blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.tittle
    
class survey(models.Model):
    """this is the model's survey"""
    answers = models.JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)