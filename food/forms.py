import json
import urllib.parse
import urllib.request
import os
import environ
from django import forms
from django.conf import settings

DEFAULT_CLOSEST_PLACES = 5  # kilometers

MINIMUM_NUMBER_OF_PLACES = 1  # kilometers


class SearchForm(forms.Form):
    
    PRICE_CHOICES = (('Any', 'Any'), ('Low', 'Low'),('Medium', 'Medium'),('High', 'High'),)
    
    CUISINE_CHOICES = (('Any', 'Any'), ('Indian', 'Indian'), ('Chinese', 'Chinese'),('Thai', 'Thai'),
        ('Mexican', 'Mexican'),('Western', 'Western'),('Malay', 'Malay'),('Korean', 'Korean'),
        ('Japanese', 'Japanese'),('Italian', 'Italian'), ('Indonesian', 'Indonesian'), ('Singaporean', 'Singaporean'), ('Brazilian', 'Brazilian'), ('South African', 'South African'), ('Vietnamese', 'Vietnamese'), ('French', 'French'), ('Taiwanese', 'Taiwanese'), ('Hong Kong', 'Hong Kong'), ('Others', 'Others'),)
    
    TYPE_OF_FOOD_LOCATION_CHOICES = (('Any', 'Any'), ('Bar', 'Bar'), ('Fast Food / Restaurant', 'Fast Food / Restaurant') ,
        ('Cafe', 'Cafe'),('Buffet', 'Buffet'),('Hawker', 'Hawker'),('Others', 'Others'),)

    OPTIONS_OF_FOOD_CHOICES = (('Any', 'Any'), ('Beverage', 'Beverage'), ('Dessert', 'Dessert'), ('Meal', 'Meal'), ('Snack', 'Snack'),)

    address = forms.CharField(label='Location', widget=forms.TextInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'Any address, postal code, etc.',
        'type': 'search',
    }))

    distance_limit = forms.IntegerField(min_value=1, max_value=45, initial=5, label='How far are you willing to travel (km)', widget=forms.NumberInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'How far are you willing to go?',
    })) 

    late_hours = forms.BooleanField(required=False, initial=False, label='Open after 11pm')
    
    halal = forms.BooleanField(required=False, initial=False, label='Halal')
    
    price = forms.ChoiceField(required=False, choices=PRICE_CHOICES, label='Price Range')
    
    cuisine = forms.ChoiceField(required=False, choices=CUISINE_CHOICES, label='Type Of Cuisine')
    
    type_of_food = forms.ChoiceField(required=False, choices=TYPE_OF_FOOD_LOCATION_CHOICES, label='Type Of Location')
   
    option_of_food = forms.ChoiceField(required=False, choices=OPTIONS_OF_FOOD_CHOICES, label='Type Of Food')

    randoming = forms.BooleanField(required=False, initial=False, label="I'm too indecisive for choices")

    def get_point(self, address):
        outputFormat = 'json'
        parameters = urllib.parse.urlencode({
            'address': address + '+singapore',
            'key': os.environ['google_api_key'],
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
        ('Japanese', 'Japanese'),('Italian', 'Italian'), ('Indonesian', 'Indonesian'), ('Singaporean', 'Singaporean'), ('Brazilian', 'Brazilian'), ('South African', 'South African'), ('Vietnamese', 'Vietnamese'), ('French', 'French'), ('Taiwanese', 'Taiwanese'), ('Hong Kong', 'Hong Kong'), ('Others', 'Others'),)
    TYPE_OF_FOOD_LOCATION_CHOICES = (('Bar', 'Bar'), ('Beverage', 'Beverage'), ('Fast Food / Restaurant', 'Fast Food / Restaurant'), ('Dessert', 'Dessert'),
        ('Cafe', 'Cafe'),('Buffet', 'Buffet'),('Snack', 'Snack'),('Hawker', 'Hawker'),('Others', 'Others'),)

    OPTIONS_OF_FOOD_CHOICES = (('Any', 'Any'), ('Beverage', 'Beverage'), ('Dessert', 'Dessert'), ('Meal', 'Meal'), ('Snack', 'Snack'),)

    address = forms.CharField(label='Location', widget=forms.TextInput(attrs={
        'placeholder': 'Any address, postal code, etc.',
        'type': 'search',
    }))
    late_hours = forms.BooleanField(required=False, initial=False, label='Opens after 11pm')
    price = forms.ChoiceField(required=False, choices=PRICE_CHOICES)
    cuisine = forms.ChoiceField(required=False, choices=CUISINE_CHOICES)
    type_of_food = forms.ChoiceField(required=False, choices=TYPE_OF_FOOD_LOCATION_CHOICES)
    option_of_food = forms.ChoiceField(required=False, choices=OPTIONS_OF_FOOD_CHOICES, label='Type Of Food')
    halal = forms.BooleanField(required=False, initial=False, label='Halal')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    open_hours = forms.CharField(required=False, label='Opening Hours', widget=forms.Textarea(attrs={"rows":2, "cols":20}))

    def get_point(self, address):
        outputFormat = 'json'
        parameters = urllib.parse.urlencode({
            'address': address + '+singapore',
            'key': os.environ['google_api_key'],
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

class TagForm(forms.Form):

    address = forms.CharField(label='Location', widget=forms.TextInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'Any address, postal code, etc.',
        'type': 'search',
    }))

    distance_limit = forms.IntegerField(min_value=1, max_value=45, initial=5, label='How far away (km)', widget=forms.NumberInput(attrs={
        'class' 'form-control mb-3'
        'placeholder': 'How far are you willing to go?',
    }))

    PRICE_CHOICES = (('Any', 'Any'), ('Low', 'Low'),('Medium', 'Medium'),('High', 'High'),)

    price = forms.ChoiceField(required=False, choices=PRICE_CHOICES)

    late_hours = forms.BooleanField(required=False, initial=False, label='Open after 11pm')

    halal = forms.BooleanField(required=False, initial=False, label='Halal')

    def get_point(self, address):
        outputFormat = 'json'
        parameters = urllib.parse.urlencode({
            'address': address + 'singapore',
            'key': os.environ['google_api_key'],
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

