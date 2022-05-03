from django.db import models
from user.models import ExtUser


class Property(models.Model):
    property_name = models.CharField(max_length=200, blank=True)
    property_contact_num = models.IntegerField()
    property_street_address = models.CharField(max_length=40, default='', blank=False, verbose_name='Street Address')
    property_city = models.CharField(max_length=20, blank=False, default='')
    property_state = models.CharField(max_length=2, blank=False, default='NE')
    property_zipcode = models.CharField(max_length=9, blank=False, default='', verbose_name='Zip Code')
    user = models.ForeignKey(ExtUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Property Manager')

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.property_name


class Apartment(models.Model):
    apartment_name = models.CharField(max_length=200, blank=True)
    apt_num = models.CharField(max_length=5, default='', blank=False, verbose_name='Apartment Number')
    size_in_sqft = models.IntegerField(default=0, blank=False, verbose_name='Size (sqft)')
    number_of_bedrooms = models.IntegerField(default=0, blank=False, verbose_name='Number of Bedrooms')
    description = models.CharField(max_length=300, default='', blank=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='Property')

    def __str__(self):
        return self.apartment_name
