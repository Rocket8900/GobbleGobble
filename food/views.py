from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, FormView, FormMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import random

# GEODJANGO IMPORTS

# For annotating and calculating distance
from django.contrib.gis.db.models.functions import Distance

# For filtering queryset based on distance provided
from django.contrib.gis.measure import D

# For Using Point on a map
from django.contrib.gis.geos import Point

from django.db.models import Q 
from django.core.paginator import Paginator

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# from django.contrib import messages

from .forms import SearchForm, ShopForm
from .models import shop, Cuisine, Price, Type_of_food, Type_of_item
from .utils import random_string_generator

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from taggit.models import Tag

# GENERAL VIEWS

def Home(request):
	return render(request, 'food/home.html')

def Explore(request):
	return render(request, 'food/explore.html')

def Search(request):
	return render(request, 'food/search.html')

def Error(request):
	return render(request, 'food/errorfinding.html')

def SaveError(request):
	return render(request, 'food/saveerror.html')

def About(request):
	return render(request, 'food/about.html')

def Contact(request):
	return render(request, 'food/contact.html')

def Privacy(request):
	return render(request, 'food/privacy.html')

def is_valid_queryparam(param):
	return param != '' and param is not None

def handler404(request, exception):
    return render(request, 'food/404.html', status=404)

def handler500(request):
    return render(request, 'food/500.html', status=500)

# def handler403(request):
#     return render(request, 'food/403.html', status=403)

# LOGIN SECTION

class CustomLoginView(LoginView):
	template_name = 'food/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('food:food_list')

class RegisterPage(FormView):
	template_name = 'food/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('food:food_list')

	def form_valid(self,form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)

	def get (self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('food:food_list')
		return super(RegisterPage, self).get(*args, **kwargs)

# COMMUNITY SECTION

class CommunityfullListView(ListView):
	model = shop
	template_name = 'food/communitylist.html'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset().filter(user='1')

		search_input = self.request.GET.get('Search') or ''
		print(search_input)
		if search_input:
			queryset = queryset.filter(name__icontains=search_input)
			
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# print(context)

		paginator = context['paginator']
		page_numbers_range = 10  # Display 5 page numbers
		max_index = len(paginator.page_range)

		page = self.request.GET.get('page')
		# print (self.request)
		current_page = int(page) if page else 1

		start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
		end_index = start_index + page_numbers_range
		if end_index >= max_index:
			end_index = max_index

		page_range = paginator.page_range[start_index:end_index]
		context['page_range'] = page_range

		return context

class CommunityListView(FormMixin, ListView):
	model = shop
	form_class = SearchForm
	template_name = 'food/communitysearch.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['object_list'] = context['object_list'].filter(user='1')


		return context

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		# if 'random' in request.GET:
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

		return response 

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.request.method == 'GET' and self.request.GET:
			kwargs['data'] = self.request.GET
		# if 'random' in self.request.POST:
		# 	print('this is random')
		return kwargs

	def form_valid(self, form):
		kwargs = {
			'query': form.cleaned_data['address'],
		#	'radius': form.cleaned_data['Number_of_places_nearby'], 
		}
		point = form.get_point(kwargs['query'])
		late_hours = self.request.GET.get('late_hours')
		price = self.request.GET.get('price')
		cuisine = self.request.GET.get('cuisine')
		type_of_food = self.request.GET.get('type_of_food')
		option_of_food = self.request.GET.get('option_of_food')
		halal = self.request.GET.get('halal')
		distance_limit = self.request.GET.get('distance_limit')
		randoming = self.request.GET.get('randoming')
		object_list = shop.objects.all()
		context = {'object_list': object_list}
		print(context)

		if point:
			kwargs['point'] = point			
			user_location = Point(point['longitude'], point['latitude'], srid=4326)
			kwargs['object_list'] = super().get_queryset().annotate(distance=Distance(user_location,
   'location')
    ).order_by('distance')

		# else:
		# 	return redirect('food:error')
		
		if is_valid_queryparam(price) and price != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(price__costs=price)

		if late_hours == 'on':
			kwargs['object_list'] = kwargs['object_list'].filter(late_hours=True)

		if halal == 'on':
			kwargs['object_list'] = kwargs['object_list'].filter(halal=True)

		if is_valid_queryparam(cuisine) and cuisine != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(cuisine__options=cuisine)

		if is_valid_queryparam(type_of_food) and type_of_food != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(type_of_food__variety=type_of_food)

		if is_valid_queryparam(option_of_food) and option_of_food != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(type_of_item__choices=option_of_food)

		kwargs['object_list'] = kwargs['object_list'].filter(location__distance_lte=(user_location, D(km=distance_limit)))

		if randoming == 'on':
			randomised_list = kwargs['object_list'].order_by('?').first()
			kwargs['object_list'] = kwargs['object_list'].filter(name__icontains=randomised_list.name)
				
		kwargs['object_list'] = kwargs['object_list']
		return self.render_to_response(self.get_context_data(**kwargs))

class CommunityDetailView(FormMixin, DetailView):
	model = shop
	template_name = 'food/community_detail.html'
	form_class = SearchForm

	def get (self, *args, **kwargs):
		person = self.get_object().user.id
		# print(person)
		if person == 1:
			return super(CommunityDetailView, self).get(*args, **kwargs)
		else:
		 	return redirect('food:community_list')

def save_to_me(request,id):
	user = request.user
	# places = shop.objects.all()
	# place_name = places.name
	# print(place_name)
	destination = get_object_or_404(shop, id=id)
	# print(destination)
	if user == '':
		return redirect('communitylist/')
	else:
		name = destination.name
		location= destination.location
		price = destination.price
		cuisine = destination.cuisine
		type_of_food = destination.type_of_food
		type_of_item = destination.type_of_item
		late_hours = destination.late_hours
		new_slug = destination.slug
		address = destination.address
		directions = destination.directions
		halal = destination.halal
		description = destination.description
		referrence_Number = destination.referrence_Number

		slug = "{name}{randstr}".format(
				name = new_slug,
				randstr=random_string_generator(size=4)
			)


		ins = shop(user=user, name=name, location=location, price=price, cuisine=cuisine, type_of_food=type_of_food, type_of_item=type_of_item, late_hours=late_hours, slug=slug, address=address, directions=directions, halal=halal, description=description, referrence_Number=referrence_Number)
		try:
			ins.save()
		except IntegrityError as err:
			# raise ValidationError('The pools are all full.')
			return HttpResponseRedirect(reverse('food:saveerror'))



		# return redirect('food:community_list')
		return HttpResponseRedirect(reverse('food:community_list'))
		# return HttpResponseRedirect(request.META['HTTP_REFERER'])

# PERSONAL LIST SECTION

class AllListView(LoginRequiredMixin, ListView):
	model = shop
	template_name = 'food/foodlist.html'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset().filter(user=self.request.user)

		search_input = self.request.GET.get('Search') or ''
		print(search_input)
		if search_input:
			queryset = queryset.filter(name__icontains=search_input)
			
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# print(context)

		paginator = context['paginator']
		page_numbers_range = 10  # Display 5 page numbers
		max_index = len(paginator.page_range)

		page = self.request.GET.get('page')
		# print (self.request)
		current_page = int(page) if page else 1

		start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
		end_index = start_index + page_numbers_range
		if end_index >= max_index:
			end_index = max_index

		page_range = paginator.page_range[start_index:end_index]
		context['page_range'] = page_range

		return context

class FoodDetailView(FormMixin, DetailView):
	model = shop
	template_name = 'food/food_detail.html'
	form_class = SearchForm

	# def get_context_data(self, **kwargs):
	# 	context['previous'] = self.request.META.get('HTTP_REFERER', reverse('food:food_list'))
	# 	return context

	def get (self, *args, **kwargs):
		user = self.request.user.id
		person = self.get_object().user.id
		print(user)
		print(person)
		if person == 2:
			print('nice person is 2')
		if user == person or person == 2:
			return super(FoodDetailView, self).get(*args, **kwargs)
		else:
			return redirect('food:food_list')

	# def form_valid(self, form):
	# 	kwargs = {
	# 		'query': form.cleaned_data['address'],
	# 	}
	# 	point = form.get_point(kwargs['query'])

	# 	if point:
	# 		kwargs['point'] = point			
	# 		location_position = Point(point['formatted_address'])
	# 		print(location_position)
	# 		kwargs['object_list'] = super().get_queryset().annotate(distance=Distance(user_location,
 #  			'location')
 #    		).order_by('distance')

	# 	return self.render_to_response(self.get_context_data(**kwargs))


	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['object_list'] = context['object_list'].filter(user=self.request.user)

	# 	# search_input = self.request.GET.get('Search') or ''
	# 	# if search_input:
	# 	# 	context['object_list'] = context['object_list'].filter(name__icontains=search_input)

	# 	return context

class FoodListView(LoginRequiredMixin, FormMixin, ListView):
	model = shop
	form_class = SearchForm
	template_name = 'food/foodsearch.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = context['object_list'].filter(user=self.request.user)

		# search_input = self.request.GET.get('Search') or ''
		# if search_input:
		# 	context['object_list'] = context['object_list'].filter(name__icontains=search_input)

		return context

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		# if 'random' in request.GET:
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

		return response 

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.request.method == 'GET' and self.request.GET:
			kwargs['data'] = self.request.GET
		# if 'random' in self.request.POST:
		# 	print('this is random')
		return kwargs

	def form_valid(self, form):
		kwargs = {
			'query': form.cleaned_data['address'],
		#	'radius': form.cleaned_data['Number_of_places_nearby'], 
		}
		point = form.get_point(kwargs['query'])
		late_hours = self.request.GET.get('late_hours')
		price = self.request.GET.get('price')
		cuisine = self.request.GET.get('cuisine')
		type_of_food = self.request.GET.get('type_of_food')
		option_of_food = self.request.GET.get('option_of_food')
		halal = self.request.GET.get('halal')
		distance_limit = self.request.GET.get('distance_limit')
		randoming = self.request.GET.get('randoming')

		if point:
			kwargs['point'] = point			
			user_location = Point(point['longitude'], point['latitude'], srid=4326)
			kwargs['object_list'] = super().get_queryset().annotate(distance=Distance(user_location,
   'location')
    ).order_by('distance')

		# else:
		# 	return redirect('food:error')
		
		if is_valid_queryparam(price) and price != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(price__costs=price)

		if late_hours == 'on':
			kwargs['object_list'] = kwargs['object_list'].filter(late_hours=True)

		if halal == 'on':
			kwargs['object_list'] = kwargs['object_list'].filter(halal=True)

		if is_valid_queryparam(cuisine) and cuisine != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(cuisine__options=cuisine)

		if is_valid_queryparam(type_of_food) and type_of_food != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(type_of_food__variety=type_of_food)

		if is_valid_queryparam(option_of_food) and option_of_food != 'Any':
			kwargs['object_list'] = kwargs['object_list'].filter(type_of_item__choices=option_of_food)


		kwargs['object_list'] = kwargs['object_list'].filter(location__distance_lte=(user_location, D(km=distance_limit)))

		if randoming == 'on':
			randomised_list = kwargs['object_list'].order_by('?').first()
			kwargs['object_list'] = kwargs['object_list'].filter(name__icontains=randomised_list.name)
			# kwargs['object_list'] = kwargs['object_list'].filter(randomised_list)
			# for i in range(1):
			# 	kwargs['object_list'] = random.choice(kwargs['object_list'])
				
		kwargs['object_list'] = kwargs['object_list']
		return self.render_to_response(self.get_context_data(**kwargs))

class FoodUpdate(LoginRequiredMixin, UpdateView):
	model = shop
	fields  = ['name', 'address', 'description', 'cuisine', 'price', 'late_hours'] 
	template_name = 'food/update_form.html'
	success_url = reverse_lazy('food:food_list')

	def get (self, *args, **kwargs):
		user = self.request.user.id
		person = self.get_object().user.id
		if user == person:
			return super(FoodUpdate, self).get(*args, **kwargs)
		else:
			return redirect('food:food_list')


class DeleteView(LoginRequiredMixin, DeleteView):
	model = shop
	context_object_name = 'shop'
	success_url = reverse_lazy('food:food_list')

# Addition of extra places

class showform(LoginRequiredMixin, FormView):
	template_name = 'food/addplaces.html'
	form_class = ShopForm
	success_url = reverse_lazy('food:food_list')

	def form_valid(self, form):
		kwargs = {
				'query': form.cleaned_data['address'],
			}
		point = form.get_point(kwargs['query'])

		if point:
			kwargs['point'] = point
			location = Point(point['longitude'], point['latitude'], srid=4326)
			
			lon = point['longitude']
			lat = point['latitude']

			name = self.request.POST['name']

			user = self.request.user
			
			late_hours = form.cleaned_data['late_hours']

			halal = form.cleaned_data['halal']

			address = point['formatted_address']

			cuisine = self.request.POST['cuisine']
			cuisine = Cuisine.objects.get(options=cuisine)
				
			price = self.request.POST['price']
			price = Price.objects.get(costs=price)

			type_of_food = self.request.POST['type_of_food']
			type_of_food = Type_of_food.objects.get(variety=type_of_food)

			type_of_item = self.request.POST['option_of_food']
			type_of_item = Type_of_item.objects.get(choices=type_of_item)

			description = self.request.POST['description']

			open_hours = self.request.POST['open_hours']

			directions = "http://maps.google.com/maps?z=12&t=m&q=loc:"+str(lat)+"+"+str(lon)

			slug = "{name}-{randstr}".format(
				name = name,
				randstr=random_string_generator(size=4)
			)
			
			ins = shop(user=user, name=name, location=location, price=price, cuisine=cuisine, type_of_food=type_of_food, type_of_item=type_of_item, late_hours=late_hours, slug=slug, address=address, directions=directions, halal=halal, description=description ,open_hours=open_hours)
			print(ins)
			ins.save()
			# messages.add_message(self.request, messages.SUCCESS, "Todo added successfully")

		else:
			print('cant retrieve the point')


		context = {
    	    'form': form,
    	}

		return super(showform, self).form_valid(form)


