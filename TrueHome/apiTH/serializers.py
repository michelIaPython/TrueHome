# Django-res-framework
from rest_framework import serializers
from rest_framework.exceptions import server_error

# Models
from .models import Property, Activity, survey

# Python
from datetime import datetime, date
import pytz
import re
from datetimerange import DateTimeRange


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for add a new property"""
    
    class Meta:
        model = Property
        fields = ['tittle','address','description','status']
        
class SurveySerializer(serializers.ModelSerializer):
    """Serializer for add a new survey"""

    class Meta:
        model = survey
        fields = '__all__'
        
class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for add a new property"""
    condition = serializers.SerializerMethodField('get_condition_activity')
    property = PropertySerializer(many=False, read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id','tittle','status','property','schedule','condition'] 
    def get_condition_activity(self, activity):
        
        activity_query = Activity.objects.get(pk=activity.id)
        estate = activity_query.status
        schedule_activity = (activity_query.schedule.date())
        current_date = datetime.now().date()
        condition = "Sin condicion"
        if schedule_activity >= current_date and bool(re.search(estate,'activate')):
            condition = "Pendiente a realizar"
        elif schedule_activity <= current_date and bool(re.search(estate,'activate')):
            condition = "Atrasada"
        elif bool(re.search(estate,'done')):
            condition = "Finalizada"
        return condition
    
    
    def create(self, validated_data):
        """Overide create method for make few validations"""
        
        delta_time =  datetime.timedelta(hours=1)
        activities_schedule = Activity.objects.all()
        time_range = DateTimeRange()
        for activity in activities_schedule:
            print(validated_data['schedule'])
            time_plus_one_h = activity.schedule + delta_time
            time_range = DateTimeRange(activity.schedule, time_plus_one_h)
            if validated_data['schedule'] in time_range:
                raise serializers.ValidationError('Error can not attach the activity because the time traslape ')
        canceled = validated_data['property'].disable_at
        if canceled != None:
            raise serializers.ValidationError('Error can not attach the activity because the property is deactivated ')
        return Activity.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Override the method update for just change status o schedule"""
        
        activity_data = Activity.objects.get(pk=instance.id)
        if len(validated_data) > 1:
            raise serializers.ValidationError('You can only update satatus or schedule')
        
        if "status" in validated_data:
            new_status = validated_data['status']    
            Activity.objects.filter(pk=instance.id).update(**validated_data)
            
            return activity_data
        
        elif "schedule" in validated_data:
            
            time_on_db = activity_data.schedule.time()
            date_in_frame = validated_data['schedule'].date()
            update_datetime = pytz.utc.localize(datetime.datetime.combine(date_in_frame , time_on_db))
            micro_seconds = validated_data['schedule'].time().microsecond
            act_status = activity_data.status
            
            if re.search(act_status, 'cancelada'):
                raise serializers.ValidationError('The activity is in canceled status, you can not reeschedule')
            
            if micro_seconds != 0:
                raise serializers.ValidationError('Error can not update the time')
            validated_data['schedule'] = update_datetime
            Activity.objects.filter(pk=instance.id).update(**validated_data)
            
            return activity_data
        