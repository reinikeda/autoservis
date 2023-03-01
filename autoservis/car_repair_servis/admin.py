from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class CarModelsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', )
    list_display_links = ('model', )
    search_fields = ('brand', 'model', )

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'year', 'engine', 'color', 'plate_number', 'vin_number', 'client', 'customer', )
    list_filter = ('client', 'engine', )
    search_fields = ('customer__last_name', )
    list_editable = ('engine', 'color', )
    fieldsets = (
        (_('General'), {'fields': ('car_model', 'year', 'engine', 'color')}),
        (_('Registration'), {'fields': ('client', 'customer', 'plate_number', 'vin_number')})
    )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', )
    search_fields = ('name', )
    list_editable = ('price', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date_start', 'status', 'is_overdue', 'date_finish', 'total_order_sum', )
    list_filter = ('status', )
    list_editable = ('status', 'date_finish', )

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'order', 'quantity', 'total_price', )
    list_display_links = ('order', )
    list_filter = ('service', )
    list_editable = ('quantity', )

    @admin.display(description='Service name')
    def service_name(self, obj):
        return obj.service.name

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order', 'reviewer', 'content', )
    list_display_links = ('created_at', )
    list_filter = ('order', )
    search_fields = ('reviewer__last_name', 'order__car')

admin.site.register(models.CarModel, CarModelsAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.OrderReview, OrderReviewAdmin)