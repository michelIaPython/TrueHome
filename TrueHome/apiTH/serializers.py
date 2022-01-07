# Django-res-framework
from rest_framework import serializers

# Models
from .models import Property, Activity, survey

# Python
from datetime import datetime
import datetime as date_time
import pytz
import re
from datetimerange import DateTimeRange
class PropertySerializer(serializers.ModelSerializer):
    """Serializer for add a new property"""
    class Meta:
        model = Property
        fields = '__all__'

class surveyDataSerializer(serializers.ModelSerializer):
    """Serializer for survey like data"""
    class Meta:
        model= survey
        fields = '__all__'
        
class SurveySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for add a new survey like link"""
    class Meta:
        model = survey
        fields = ['url']
        
class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for add a new property"""
    condition = serializers.SerializerMethodField('get_condition_activity', 
                                                  read_only=True)
    survey = SurveySerializer(many=False,
                              read_only=True)
    property_data = serializers.SerializerMethodField('get_data_property',
                                                      read_only=True)
    class Meta:
        model = Activity
        fields = '__all__'
        fields = ['id','tittle','status',
                  'property','schedule','condition',
                  'property_data','survey']
        
    def get_data_property(self, activity):
        """Get a new field for data of property"""
        
        return_dict = {}
        property_query = Property.objects.get(pk=activity.property.id)
        return_dict['id'] = property_query.id
        return_dict['tittle'] = property_query.tittle
        return_dict['address'] = property_query.address
        return return_dict
    
    def get_condition_activity(self, activity):
        """Get a new field for condition"""
        
        activity_query = Activity.objects.get(pk=activity.id)
        estate = activity_query.status
        schedule_activity = (activity_query.schedule.date())
        current_date = datetime.now().date()
        active = bool(re.search(estate,'active'))
        done = bool(re.search(estate,'done'))
        condition = "Sin condicion"
        if schedule_activity >= current_date and active:
            condition = "Pendiente a realizar"
        elif schedule_activity <= current_date and active:
            condition = "Atrasada"
        elif done:
            condition = "Finalizada"
        return condition
    
    def create(self, validated_data):
        """Overide create method for make few validations"""
        
        delta_time =  date_time.timedelta(hours=1)
        activities_schedule = Activity.objects.all()
        time_range = DateTimeRange()
        for activity in activities_schedule:
            time_plus_one_h = activity.schedule + delta_time
            time_range = DateTimeRange(activity.schedule, time_plus_one_h)
            if validated_data['schedule'] in time_range:
                raise serializers.ValidationError("Error can not attach the" 
                                                  "activity because the time " 
                                                  "traslape ")
        canceled = validated_data['property'].disable_at
        if canceled != None:
            raise serializers.ValidationError("Error can not attach the "
                                              "activity because the property is"
                                              " deactivated ")
        return Activity.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Override the method update for just change status o schedule"""
        
        activity_data = Activity.objects.get(pk=instance.id)
        if len(validated_data) > 1:
            raise serializers.ValidationError("You can only update"
                                              " satatus or schedule")
        
        if "status" in validated_data:
            
            new_status = validated_data['status']    
            Activity.objects.filter(pk=instance.id).update(**validated_data)
            
            return activity_data
        
        elif "schedule" in validated_data:
            
            time_on_db = activity_data.schedule.time()
            date_in_frame = validated_data['schedule'].date()
            update_datetime = pytz.utc.localize(datetime.combine(date_in_frame, 
                                                                 time_on_db))
            act_status = activity_data.status
            
            if re.search(act_status, 'cancelada'):
                raise serializers.ValidationError("The activity is in canceled "
                                                  "status, you can not "
                                                  "reeschedule")
                
            validated_data['schedule'] = update_datetime
            Activity.objects.filter(pk=instance.id).update(**validated_data)
            
            return activity_data