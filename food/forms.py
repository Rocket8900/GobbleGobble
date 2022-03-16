import json
import urllib.parse
import urllib.request

from django import forms
from django.conf import settings

DEFAULT_CLOSEST_PLACES = 5  # kilometers

MINIMUM_NUMBER_OF_PLACES = 1  # kilometers


class SearchForm(forms.Form):
    
    PRICE_CHOICES = (('Choose', 'Choose'), ('Low', 'Low'),('Medium', 'Medium'),('High', 'High'),)
    
    CUISINE_CHOICES = (('Choose', 'Choose'), ('Indian', 'Indian'), ('Chinese', 'Chinese'),('Thai', 'Thai'),
        ('Mexican', 'Mexican'),('Western', 'Western'),('Malay', 'Malay'),('Korean', 'Korean'),
        ('Japanese', 'Japanese'),('Italian', 'Italian'),('Vietnamese', 'Vietnamese'),('Others', 'Others'),)
    
    TYPE_OF_FOOD_LOCATION_CHOICES = (('Choose', 'Choose'), ('Bar', 'Bar'),('Restaurant', 'Restaurant'),('Fast Food', 'Fast Food'),('Desert', 'Desert'),
        ('Cafe', 'Cafe'),('Buffet', 'Buffet'),('Snack', 'Snack'),('Hawker', 'Hawker'),('Others', 'Others'),)


    address = forms.CharField(label='Location', widget=forms.TextInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'Any address, postal code, etc.',
        'type': 'search',
    }))

    distance_limit = forms.IntegerField(min_value=1, max_value=45, label='Distance', widget=forms.NumberInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'How far are you willing to go?',
    })) 

    late_hours = forms.BooleanField(required=False, initial=False, label='Open after 11pm')
    
    halal = forms.BooleanField(required=False, initial=False, label='Halal')
    
    price = forms.ChoiceField(required=False, choices=PRICE_CHOICES, label='Price Range')
    
    cuisine = forms.ChoiceField(required=False, choices=CUISINE_CHOICES, label='Type Of Cuisine')
    
    type_of_food = forms.ChoiceField(required=False, choices=TYPE_OF_FOOD_LOCATION_CHOICES, label='Type Of Location')
   
    randoming = forms.BooleanField(required=False, initial=False, label="I'm too indecisive for choices")

    def get_point(self, address):
        outputFormat = 'json'
        parameters = urllib.parse.urlencode({
            'address': address + 'singapore',
            'key': settings.GOOGLE_API_KEY,
        })
        url = 'https://maps.googleapis.com/maps/api/geocode/%s?%s' % (outputFormat, parameters)
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read().decode('utf-8'))
            if body['status'] == 'OK':
                try:
                    return {
                        'latitude': body['results'][0]['geometry']['location']['lat'],
                        'longitude': body['results'][0]['geometry']['location']['lng'],
                        'formatted_address': body['results'][0]['formatted_address'],
                    }
                except KeyError:
                    return {}
                except IndexError:
                    return {}
            return {}

class ShopForm(forms.Form):
    name = forms.CharField()
    PRICE_CHOICES = (('Low', 'Low'),('Medium', 'Medium'),('High', 'High'),)
    CUISINE_CHOICES = (('Indian', 'Indian'), ('Chinese', 'Chinese'),('Thai', 'Thai'),
        ('Mexican', 'Mexican'),('Western', 'Western'),('Malay', 'Malay'),('Korean', 'Korean'),
        ('Japanese', 'Japanese'),('Italian', 'Italian'),('Vietnamese', 'Vietnamese'),('Others', 'Others'),)
    TYPE_OF_FOOD_LOCATION_CHOICES = (('Bar', 'Bar'),('Restaurant', 'Restaurant'),('Fast Food', 'Fast Food'),('Desert', 'Desert'),
        ('Cafe', 'Cafe'),('Buffet', 'Buffet'),('Snack', 'Snack'),('Hawker', 'Hawker'),('Others', 'Others'),)


    address = forms.CharField(label='Location', widget=forms.TextInput(attrs={
        'placeholder': 'Any address, postal code, etc.',
        'type': 'search',
    }))
    late_hours = forms.BooleanField(required=False, initial=False, label='Opens after 11pm')
    price = forms.ChoiceField(required=False, choices=PRICE_CHOICES)
    cuisine = forms.ChoiceField(required=False, choices=CUISINE_CHOICES)
    type_of_food = forms.ChoiceField(required=False, choices=TYPE_OF_FOOD_LOCATION_CHOICES)
    halal = forms.BooleanField(required=False, initial=False, label='Halal')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    def get_point(self, address):
        outputFormat = 'json'
        parameters = urllib.parse.urlencode({
            'address': address + 'singapore',
            'key': settings.GOOGLE_API_KEY,
        })
        url = 'https://maps.googleapis.com/maps/api/geocode/%s?%s' % (outputFormat, parameters)
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read().decode('utf-8'))
            if body['status'] == 'OK':
                try:
                    return {
                        'latitude': body['results'][0]['geometry']['location']['lat'],
                        'longitude': body['results'][0]['geometry']['location']['lng'],
                        'formatted_address': body['results'][0]['formatted_address'],
                    }
                except KeyError:
                    return {}
                except IndexError:
                    return {}
            return {}



