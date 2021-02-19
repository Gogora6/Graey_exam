from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ecommerce.forms import OrderForm
from ecommerce.models import Order, Ticket

from .choices import TicketStatus


def index(request: WSGIRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('user:login')
    return render(request, 'pages/ecommerce/index.html')


@login_required
def orders_list(request: WSGIRequest) -> HttpResponse:
    orders: Order = Order.objects.filter(user_id=request.user.pk)
    return render(request, 'pages/ecommerce/orders.html', context={'orders': orders})


@login_required
def create_orders(request: WSGIRequest) -> HttpResponse:
    order_form = OrderForm()
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order: Order = order_form.save(commit=False)
            order.user_id = request.user.id
            order.save()
            ticket = Ticket.objects.get(id=order.ticket_id)
            ticket.status = TicketStatus.unavailable
            ticket.save()
            return redirect('ecommerce:orders_list')

    return render(request, 'pages/ecommerce/create-orders.html', context={'form': order_form})


@login_required
def ticket_list(request: WSGIRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    tickets: Ticket = Ticket.objects.filter(status=TicketStatus.available)
    paginator = Paginator(tickets, 10)
    tickets = paginator.page(page)
    return render(request, 'pages/ecommerce/tickets.html', context={'tickets': tickets})
