from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class CarModelsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'engine')
    list_display_links = ('model', )
    list_filter = ('engine', 'year', )
    search_fields = ('brand', 'model')
    list_editable = ('engine', )

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'plate_number', 'vin_number', 'client')
    list_filter = ('client', )
    list_editable = ('client', )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', )
    list_editable = ('price', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date_start', 'status', 'date_finish', 'total_order_sum')
    list_filter = ('status', )
    list_editable = ('status', 'date_finish')

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'order', 'quantity', 'total_price')
    list_display_links = ('order', )
    list_filter = ('service', )
    list_editable = ('quantity', )

    @admin.display(description='Service name')
    def service_name(self, obj):
        return obj.service.name

admin.site.register(models.CarModel, CarModelsAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)