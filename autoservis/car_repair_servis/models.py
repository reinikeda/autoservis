from django.db import models
from django.utils.translation import gettext_lazy as _

class CarModel(models.Model):
    brand = models.CharField(_('brand'), max_length=50)
    model = models.CharField(_('model'), max_length=50)
    year = models.IntegerField(_('year'))

    ENGINE = (
        ('u', _('unknown')),
        ('d', _('diesel')),
        ('p', _('petrol')),
        ('g', _('petrol and gas')),
        ('e', _('electric')),
        ('h', _('hybrid')),
    )

    engine = models.CharField(_('engine'), max_length=1, choices=ENGINE, default='u')

    def __str__(self) -> str:
        return f'{self.brand} {self.model} ({self.year}, {self.engine})'

    class Meta:
        ordering = ['brand', 'model']

class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name='cars',
        verbose_name=_('car model')
    )
    plate_number = models.CharField(_('plate number'), max_length=10)
    vin_number = models.CharField(_('VIN number'), max_length=17, help_text='VIN code must be 17 symbols long')
    client = models.CharField(_('client name'), max_length=50)
    car_image = models.ImageField(_('car image'), upload_to='car_repair_servis/cars/', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.car_model} {self.plate_number} {self.client}'

    class Meta:
        ordering = ['client', 'car_model']

class Service(models.Model):
    name = models.CharField(_('service name'), max_length=50)
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