from django.contrib import admin

# from .models import related models
from djangoapp.models import CarMake, CarModel


# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel


# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    # CarMakeAdmin class with CarModelInline
    inlines = [
        CarModelInline,
    ]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
