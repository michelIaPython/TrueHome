# Dajngo rest framework
from rest_framework.test import APITestCase
from rest_framework import status

# Models
from .models import Activity, Property, survey

# Python 
import json
class ActivityTestCase(APITestCase):

    def setUp(self):
        """Test case set up."""
        
        self.property = Property.objects.create(
            tittle = "Test Property",
            address = "Address Test",
            description = "Test case of a property",
            status = "active"
        )

    def test_registerActivity(self):
        
        url = '/api/activity/'
        data = {
            "tittle":"Test Activity",
            "status":"active",
            "property":self.property.id,
            "schedule":"2022-01-07T11:00:00Z"
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_response_succes_all(self):
        url = '/api/activity/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
    def  test_activities_same_time(self):
        url = '/api/activity/'
        data = {
            "tittle":"Test Activity",
            "status":"active",
            "property":self.property.id,
            "schedule":"2022-01-07T11:00:00Z"
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_aux = {
            "tittle":"Test Activity 2",
            "status":"active",
            "property":self.property.id,
            "schedule":"2022-01-07T11:00:00Z"
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_status_activty_and_id_property(self):
        url = '/api/activity/'
        data = {
            "tittle":"Test Activity",
            "status":"active",
            "property":self.property.id,
            "schedule":"2022-01-07T11:00:00Z"
            }
        response = self.client.post(url, data)
        self.assertEqual(response.data["status"], "active")
        self.assertEqual(response.data["property"], self.property.id)
class CreateAll(APITestCase):
    
    def test_create_activity_property_survey(self):
        url_property = '/api/property/'
        property = {
            "tittle":"Test Property",
            "address":"Address Test",
            "description":"Test case of a property",
            "status":"active"
            }
        response = self.client.post(url_property, property)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_activity = '/api/activity/'
        activity = {
            "tittle":"Test Activity",
            "status":"active",
            "property":response.data["id"],
            "schedule":"2022-01-07T11:00:00Z"
            }
        response = self.client.post(url_activity, activity)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_survey = '/api/survey/'
        json_survey = json.dumps({"Test":"Test"})
        survey = {
            "answers":json_survey,
            "activity" : response.data["id"]
        }
        response = self.client.post(url_survey, survey)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class UpdateActivity(APITestCase):
    
    def setUp(self):
                
        self.property = Property.objects.create(
            tittle = "Test Property",
            address = "Address Test",
            description = "Test case of a property",
            status = "active"
        )
        self.activity = Activity.objects.create(
            tittle = "Test Activity",
            status = "active",
            property = self.property,
            schedule= "2022-01-07T11:00:00Z"
        )
        json_survey = json.dumps({"Test":"Test"})
        self.survey =survey.objects.create( 
            answers = json_survey,
            activity = self.activity
        )
    def test_update_status(self):
        id = self.activity.id
        url = f"/api/activity/{id}/"
        data = {"status":"done"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_status(self):
        id = self.activity.id
        url = f"/api/activity/{id}/"
        data = {"schedule":"2023-01-07"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_many_fields(self):
        id = self.activity.id
        url = f"/api/activity/{id}/"
        data = {"schedule":"2023-01-07","status":"done"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        