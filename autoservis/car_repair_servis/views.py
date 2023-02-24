from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from . import models

def index(request):
    service_count = models.Service.objects.count()
    service_list = models.Service.objects.all()
    client_count = models.Car.objects.values('client').distinct().count()
    order_count = models.Order.objects.count()
    order_progress = models.Order.objects.filter(status='w').count()
    order_done = models.Order.objects.filter(status='d').count()
    model_popular = models.CarModel.objects.all()
    return render(request, 'car_repair_servis/index.html', {
        'service_count': service_count,
        'service_list': service_list,
        'client_count': client_count,
        'order_count': order_count,
        'order_progress': order_progress,
        'order_done': order_done,
        'model_popular': model_popular,
    })


class CarListView(generic.ListView):
    model = models.Car
    paginate_by = 10
    template_name = 'car_repair_servis/car_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(car_model__brand__icontains=query) |
                Q(car_model__model__icontains=query)
            )
        return qs

class CarDetailView(generic.DetailView):
    model = models.Car
    template_name = 'car_repair_servis/car_details.html'

class OrderListView(generic.ListView):
    model = models.Order
    template_name = 'car_repair_servis/order_list.html'

class OrderDetailView(generic.DetailView):
    model = models.Order
    template_name = 'car_repair_servis/order_detail.html'

class ClientListView(generic.ListView):
    model = models.Car
    template_name = 'car_repair_servis/client_list.html'

class ClientDetailView(generic.DetailView):
    model = models.Car
    template_name = 'car_repair_servis/client_detail.html'