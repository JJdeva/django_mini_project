from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Review
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['title']
admin.site.register(User, UserAdmin)

admin.site.register(Review, ReviewAdmin)