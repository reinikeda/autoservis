from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from . forms import OrderReviewForm, UserOrderCreateForm, UserOrderUpdateForm
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

class CarDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Car
    template_name = 'car_repair_servis/car_details.html'
    form_class = OrderReviewForm

    def get_success_url(self) -> str:
        return reverse_lazy('car', kwargs={'pk': self.get_object().id})

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
        messages.success(self.request, _('-- review posted successfully --'))
        return super().form_valid(form)

class OrderListView(generic.ListView):
    model = models.Order
    template_name = 'car_repair_servis/order_list.html'

class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Order
    template_name = 'car_repair_servis/order_detail.html'
    form_class = OrderReviewForm

    def get_success_url(self) -> str:
        return reverse_lazy('order', kwargs={'pk': self.get_object().id})

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
        messages.success(self.request, _('-- review posted successfully --'))
        return super().form_valid(form)

class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = models.Car
    paginate_by = 10
    template_name = 'car_repair_servis/user_car_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs
    
class UserOrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Order
    template_name = 'car_repair_servis/user_order_create.html'
    form_class = UserOrderCreateForm
    success_url = reverse_lazy('user_cars')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['car'].queryset = form.fields['car'].queryset.filter(customer=self.request.user)
        return form
        
    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'n'
        if self.request.GET.get('car_id'):
            initial['car'] = get_object_or_404(models.Car, id=self.request.GET.get('car_id'))
        initial['date_finish'] = date.today() + timedelta(days=7)
        return initial
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.status = 'n'
        messages.success(self.request, f'{_("succesfully created new order")}: {form.instance.car}')
        return super().form_valid(form)
    
class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = models.Order
    template_name = 'car_repair_servis/user_order_update.html'
    form_class = UserOrderUpdateForm
    success_url = reverse_lazy('user_cars')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.status = 'p'
        messages.success(self.request, f'{_("succesfully paid for order")}: {form.instance.car}')
        return super().form_valid(form)
    
    def test_func(self):
        return self.get_object().car.customer == self.request.user

class UserCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = models.OrderReview
    template_name = 'car_repair_servis/user_comment_delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('car', kwargs={'pk': self.get_object().order.car.id})

    def test_func(self):
        return self.get_object().reviewer == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('comment was deleted'))
        return super().form_valid(form)