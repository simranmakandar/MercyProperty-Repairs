from django.contrib import admin
from .models import Property, Apartment


class PropertyAdmin(admin.ModelAdmin):
    model = Property
    list_display = ['property_name', 'property_contact_num', 'property_street_address',
                    'property_city', 'property_state', 'property_zipcode', 'get_user_username']
    list_filter = ['property_name', 'property_contact_num', 'property_street_address',
                   'property_city', 'property_state']
    fieldset = (
        ('Property Information', {
            'fields': ('property_name', 'property_contact_num', 'property_street_address',
                       'property_city', 'property_state', 'property_zipcode', 'user_id')
        })
    )
    add_fieldset = (
        ('Property Information', {
            'fields': ('property_name', 'property_contact_num', 'property_street_address',
                       'property_city', 'property_state', 'property_zipcode', 'user_id')
        })
    )

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.admin_order_field = 'user_name'
    get_user_username.short_description = 'User Name'


class ApartmentAdmin(admin.ModelAdmin):
    model = Apartment
    list_display = ['apartment_name', 'apt_num', 'size_in_sqft', 'number_of_bedrooms', 'description',
                    'get_property_name']
    list_filter = ['number_of_bedrooms', 'property__property_name']
    fieldset = (
        ('Apartment Information', {
            'fields': ('apt_num', 'size_in_sqft', 'number_of_bedrooms', 'description', 'property_id', 'client_id')
        })
    )
    add_fieldset = (
        ('Apartment Information', {
            'fields': ('apt_num', 'size_in_sqft', 'number_of_bedrooms', 'description', 'property_id', 'client_id')
        })
    )

    def get_property_name(self, obj):
        return obj.property.property_name

    get_property_name.admin_order_field = 'property_name'
    get_property_name.short_description = 'Property Name'


admin.site.register(Property, PropertyAdmin)
admin.site.register(Apartment, ApartmentAdmin)
