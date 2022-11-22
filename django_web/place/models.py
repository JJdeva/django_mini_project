from django.db import models


# Create your models here.
class Store(models.Model):
    store_name = models.CharField(max_length=100)
    store_address = models.CharField(max_length=100)
    store_road_address = models.CharField(max_length=100)
    store_tel = models.CharField(max_length=30, blank=True, null=True)
    store_link = models.URLField(null=True, blank=True)
    store_stars = models.FloatField(null=True, blank=True)
    store_summary = models.CharField(max_length=200, null=True, blank=True)
    store_description = models.TextField(null=True, blank=True)
    store_find = models.CharField(max_length=200, null=True, blank=True)
    store_payment = models.CharField(max_length=50, null=True, blank=True)
    store_comfortables = models.CharField(max_length=200, null=True, blank=True)
    store_thumbnail = models.ImageField(upload_to='images/restaurant', blank=True, null=True)
    store_longitude = models.FloatField(blank=True, null=True)
    store_latitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.store_name

class Menu(models.Model):
    menus = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)
    # positiveIntergerField가 0도 포함한다함
    menu_price = models.PositiveIntegerField()
    menu_img = models.ImageField(upload_to='images/menu', blank=True, null=True)
    menu_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.menu_name


class Category(models.Model):
    main_category = models.CharField(max_length=20)
    sub_category1 = models.CharField(max_length=20)
    sub_category2 = models.CharField(max_length=20, null=True, blank=True)
    categories = models.OneToOneField(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.main_category

class BusinessHours(models.Model):
    day = models.CharField(max_length=40, null=True, blank=True)
    time = models.CharField(max_length=30, null=True, blank=True)
    break_time = models.CharField(max_length=100, null=True, blank=True)
    last_order = models.CharField(max_length=100, null=True, blank=True)
    hours = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day} / {self.time}'
