from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid

# Create your models here.
from .choices import TicketStatus


class Ticket(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Ticket name'), unique=True)
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'))
    qr_code = models.CharField(max_length=254, verbose_name=_('QR Code'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"), null=True)
    status = models.IntegerField(choices=TicketStatus.choices, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.qr_code = uuid.uuid4().hex[:20].upper()
        super(Ticket, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.SET_NULL, null=True, related_name='orders')
    ticket = models.OneToOneField(to='ecommerce.Ticket', on_delete=models.PROTECT, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.ticket.price
        super(Order, self).save(*args, **kwargs)
