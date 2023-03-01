from datetime import date
from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CarModel(models.Model):
    brand = models.CharField(_('brand'), max_length=50, null=False, blank=False)
    model = models.CharField(_('model'), max_length=50, null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.brand} {self.model}'

    class Meta:
        ordering = ['brand', 'model']

class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name='cars',
        verbose_name=_('car model')
    )
    year = models.IntegerField(_('year'), null=True, blank=True)

    ENGINE = (
        ('u', _('unknown')),
        ('d', _('diesel')),
        ('p', _('petrol')),
        ('g', _('petrol and gas')),
        ('e', _('electric')),
        ('h', _('hybrid')),
    )

    engine = models.CharField(_('engine'), max_length=1, choices=ENGINE, default='u')
    color = models.CharField(_('color'), max_length=50, null=True, blank=True)
    plate_number = models.CharField(_('plate number'), max_length=10, null=False, blank=False)
    vin_number = models.CharField(_('VIN number'), max_length=17, help_text='VIN code must be 17 symbols long', null=True, blank=True)
    client = models.CharField(_('client name'), max_length=50, null=False, blank=False)
    customer = models.ForeignKey(
        User,
        verbose_name=_('customer'),
        on_delete=models.SET_NULL,
        related_name='cars',
        null=True, blank=True
    )

    car_image = models.ImageField(_('car image'), upload_to='car_repair_servis/cars/', null=True, blank=True)
    description = HTMLField(_('car description'), max_length=5000, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.car_model} {self.plate_number} {self.customer}'

    class Meta:
        ordering = ['client', 'car_model']

class Service(models.Model):
    name = models.CharField(_('service name'), max_length=50, null=False, blank=False)
    price = models.DecimalField(_('service price'), null=False, blank=False, max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name}: {self.price} €'

    class Meta:
        ordering = ['name']

class Order(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('car')
    )
    date_start = models.DateField(_('date of order placement'), auto_now_add=True)

    ORDER_STATUS = (
        ('n', _('new')),
        ('w', _('work in proggress')),
        ('d', _('done')),
        ('p', _('paid')),
        ('c', _('cancelled')),
    )
    
    status = models.CharField(_('status'), max_length=1, choices=ORDER_STATUS, default='n')
    date_finish = models.DateField(_('date of order finish'), null=True, blank=True)
    total_order_sum = models.DecimalField(_('total order sum'), max_digits=10, decimal_places=2, default=0)

    @property
    def total_order_sum(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total_price
        return total

    @property
    def is_overdue(self):
        if self.date_finish:
            return self.date_finish < date.today()
        return False

    def __str__(self) -> str:
        return f'{self.date_start} {self.car}'

    class Meta:
        ordering = ['date_start', 'car']

class OrderLine(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='order_lines',
        verbose_name=_('service')
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='order_lines',
        verbose_name=_('order')
    )
    quantity = models.IntegerField(_('quantity'), default=1)
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.service.price * self.quantity

    def __str__(self) -> str:
        return f'{self.order} {self.service}: {self.total_price} €'
    
class OrderReview(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_('order'),
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer = models.ForeignKey(
        User,
        verbose_name=_('reviewer'),
        on_delete=models.SET_NULL,
        related_name='order_reviews',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    content = models.TextField(_('content'), max_length=4000)

    def __str__(self) -> str:
        return f'{self.reviewer} - {self.created_at}'
    
    class Meta:
        ordering = ['-created_at']