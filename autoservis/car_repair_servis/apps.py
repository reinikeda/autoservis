from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CarRepairServisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car_repair_servis'
    verbose_name = _('car repair servis')
