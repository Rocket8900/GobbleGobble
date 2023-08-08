from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from .utils import create_new_ref_number
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Cuisine(models.Model):
	options = models.CharField(max_length=100)

	def __str__(self):
		return self.options

class Price(models.Model):
	costs = models.CharField(max_length=100)

	def __str__(self):
		return self.costs

class Type_of_food(models.Model):
	variety = models.CharField(max_length=100)
	
	def __str__(self):
		return self.variety

class Type_of_item(models.Model):
	choices = models.CharField(max_length=100)

	def __str__(self):
		return self.choices

class shop(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100)
	location = models.PointField()
	address = models.CharField(max_length=100, blank=True)
	slug = models.SlugField(unique=True) 
	description = RichTextField(default='nothing', blank = True)
	open_hours = models.TextField(default='unknown')
	cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True)
	price= models.ForeignKey(Price, on_delete=models.CASCADE, null=True, blank=True)
	type_of_item = models.ForeignKey(Type_of_item, on_delete=models.CASCADE, null=True, blank=True)
	type_of_food= models.ForeignKey(Type_of_food, on_delete=models.CASCADE, null=True, blank=True)
# REMOVE NULL = TRUE WHEN IN PRODUCTION 
	late_hours= models.BooleanField('Opens After 11pm', default=False)
	directions = models.CharField(max_length=100, blank = True)
	halal = models.BooleanField('Halal', default=False)
	referrence_Number 	= models.CharField(
           max_length = 10,
           blank=True,
           editable=False,
           default=create_new_ref_number
      )


	class Meta:
		ordering = ['name']

	class Meta:
		constraints = [
            models.UniqueConstraint(fields=['user', 'referrence_Number'], name='user_Referrence_Number')
        ]


	def _str_(self):
		return self.name
