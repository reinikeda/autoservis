from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.urls import reverse
from . forms import OrderReviewForm
from . import models

def index(request):
    service_count = models.Service.objects.count()
    service_list = models.Service.objects.all()
    client_count = models.Car.objects.values('client').distinct().count()
    order_count = models.Order.objects.count()
    order_progress = models.Order.objects.filter(status='w').count()
    order_done = models.Order.objects.filter(status='d').count()
    model_popular = models.CarModel.objects.all()
    request.session['visit_count'] = request.session.get('visit_count', 0) + 1
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
        brand_id = self.request.GET.get('brand_id')
        if brand_id:
            qs = qs.filter(car_model=brand_id)
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(car_model__brand__icontains=query) |
                Q(car_model__model__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = models.CarModel.objects.all()
        context.update({'brands': brands})
        brand_id = self.request.GET.get('brand_id')
        if brand_id:
            brand = get_object_or_404(models.CarModel, id=brand_id)
            context.update({'current_brand': brand})
        return context

# class CarDetailView(generic.DetailView):
#     model = models.Car
#     template_name = 'car_repair_servis/car_details.html'

class CarDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Car
    template_name = 'car_repair_servis/car_details.html'
    form_class = OrderReviewForm

    def get_success_url(self) -> str:
        return reverse('car', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        # initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.order = self.object
        form.reviewer = self.request.user
        form.save()
        messages.success(self.request, 'Review posted successfully')
        return super().form_valid(form)


class OrderListView(generic.ListView):
    model = models.Order
    template_name = 'car_repair_servis/order_list.html'

class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Order
    template_name = 'car_repair_servis/order_detail.html'
    form_class = OrderReviewForm

    def get_success_url(self) -> str:
        return reverse('order', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.order = self.object
        form.reviewer = self.request.user
        form.save()
        messages.success(self.request, 'Review posted successfully')
        return super().form_valid(form)

class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = models.Car
    template_name = 'car_repair_servis/user_car_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs
    
