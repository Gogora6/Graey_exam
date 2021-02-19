from django import forms
from django.forms import ModelChoiceField

from ecommerce.models import Order, Ticket
from .choices import TicketStatus


class OrderForm(forms.ModelForm):
    ticket = ModelChoiceField(empty_label='Choice Ticket', queryset=Ticket.objects.filter(status=TicketStatus.available))

    class Meta:
        model = Order
        fields = ('ticket',)
