from django.contrib import admin
from .models import *



# Register your models here.
class showAdminPanel_person_details(admin.ModelAdmin):
    list_display = ('age','height','weight','activity','weight_plan','meals')

class showAdminPanel_nutrition_details(admin.ModelAdmin):
    list_display = (
        'CaloriesNeeded',
        'SaturatedFatContent',
        'CholesterolContent',
        'SodiumContent',
        'CarbohydrateContent',
        'FiberContent',
        'SugarContent',
        'ProteinContent',
        'num_recomm'
        )
admin.site.register(person_details,showAdminPanel_person_details)
admin.site.register(nutrition_details,showAdminPanel_nutrition_details)
admin.site.register(namaste)