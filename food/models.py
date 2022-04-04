from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from .utils import random_string_generator
from taggit.managers import TaggableManager

# WEEKDAYS = [
#     (1, ("Monday")),
#     (2, ("Tuesday")),
#     (3, ("Wednesday")),
#     (4, ("Thursday")),
#     (5, ("Friday")),
#     (6, ("Saturday")),
#     (7, ("Sunday")),
#  ]
# class OpeningTime(models.Model):

#     weekday = models.IntegerField(
#         choices=WEEKDAYS,
#         unique=True)
#     from_hour = models.TimeField()
#     to_hour = models.TimeField()

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

class shop(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100)
	location = models.PointField()
	address = models.CharField(max_length=100, blank=True)
	slug = models.SlugField(unique=True) 
	description = models.TextField(default='nothing')
	cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True)
	price= models.ForeignKey(Price, on_delete=models.CASCADE, null=True, blank=True)
	type_of_food= models.ForeignKey(Type_of_food, on_delete=models.CASCADE, null=True, blank=True)
# REMOVE NULL = TRUE WHEN IN PRODUCTION 
	late_hours= models.BooleanField('Opens After 11pm', default=False)
	directions = models.CharField(max_length=100, blank = True)
	halal = models.BooleanField('Halal', default=False)
	# opening_times = models.ManyToManyField(OpeningTime)
	tags = TaggableManager()


	class Meta:
		ordering = ['name']

	# def save(self, *args, **kwargs):
	# 	self.slug = slugify(self.name)
	# 	super(shop, self).save(*args, **kwargs)

	def _str_(self):
		return self.name

	# def unique_slug_generator(instance, new_slug=None):

	# 	if new_slug is not None:
	# 		slug = new_slug
	# 	else:
	# 		slug = slugify(instance.name)

	# 	Klass = instance.__class__
	# 	qs_exists = Klass.objects.filter(slug=slug).exists()
	# 	if qs_exists:
	# 		new_slug = "{slug}-{randstr}".format(
	# 				slug=slug,
	# 				randstr=random_string_generator(size=4)
	# 			)
	# 	return unique_slug_generator(instance, new_slug=new_slug)
	# 	return slug

	# def unique_slug_generator(self, *args, **kwargs):

	# 	new_slug = "{self.name}-{randstr}".format(
	# 				slug=self.name,
	# 				randstr=random_string_generator(size=4)
	# 			)

	# 	self.slug = slugify(new_slug)
	# 	super(shop, self).save(*args, **kwargs)
		

	# def get_absolute_url(self):
	# 	return reverse('food:food_detail', args=[self.slug])


