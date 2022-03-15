from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from food.models import shop, Cuisine, Price, Type_of_food
from django.contrib.gis.db import models as geomodels
from .widget import LatLongWidget


# Register your models here.


@admin.register(shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

    formfield_overrides = {
        geomodels.PointField: {'widget': LatLongWidget}
    }

admin.site.register(Cuisine)
admin.site.register(Price)
admin.site.register(Type_of_food)

