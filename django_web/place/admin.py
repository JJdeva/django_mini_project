from django.contrib import admin
from .models import Store, Menu, Category, BusinessHours
# Register your models here.


class StoreAdmin(admin.ModelAdmin):
    search_fields = ['store_name']

admin.site.register(Store, StoreAdmin)

admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(BusinessHours)
