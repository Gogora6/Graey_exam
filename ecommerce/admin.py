from django.contrib import admin

from .models import Order, Ticket


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ('name', 'start_date', 'end_date', 'price', 'status')
    pass
