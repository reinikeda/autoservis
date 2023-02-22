from django.shortcuts import render
from . import models

def index(request):
    service_count = models.Service.objects.count()
    service_list = models.Service.objects.all()
    client_count = models.Car.objects.count()
    order_count = models.Order.objects.count()
    brand_popular = models.CarModel.objects.all()
    return render(request, 'car_repair_servis/index.html', {
        'service_count': service_count,
        'service_list': service_list,
        'client_count': client_count,
        'order_count': order_count,
        'brand_popular': brand_popular,
    })