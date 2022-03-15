from django.urls import path
from . import views
from .views import FoodDetailView, FoodListView, Home, FoodUpdate, DeleteView, CustomLoginView, RegisterPage, AllListView, showform, CommunityListView, CommunityfullListView, CommunityDetailView
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'food'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='food:login'), name='logout'),

    path('food/search/', views.Search, name='search'),
    path('food/explore/', views.Explore, name='explore'),

	path('', views.Home, name='home'),
    path('food/<slug>/', FoodDetailView.as_view(), name='food_detail'),
    path('food/full', AllListView.as_view(), name='list'),
    path('food/', FoodListView.as_view(), name='food_list'),
    
    path('communitylist/', CommunityListView.as_view(), name='community_list'),
    path('communitylist/full', CommunityfullListView.as_view(), name='community_full_list'),
    path('communitylist/<slug>/', CommunityDetailView.as_view(), name='community_detail'),
    path('save/<int:id>/', views.save_to_me, name='save_to_me'),

    # path('addition', views.showform, name='addition'),
    path('addition', showform.as_view(), name='addition'),
    path('food-update/<slug>/', FoodUpdate.as_view(), name='food-update'),
    path('food-delete/<slug>/', DeleteView.as_view(), name='food-delete'),
    path('error/', views.Error, name='error'),
    ]