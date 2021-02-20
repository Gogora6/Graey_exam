from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.handlers.wsgi import WSGIRequest

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ecommerce.forms import OrderForm
from ecommerce.models import Order, Ticket

from .choices import TicketStatus


@login_required(redirect_field_name=None)
def index(request: WSGIRequest) -> HttpResponse:
    now = timezone.now()
    user_orders_info = Order.objects.filter(user_id=request.user.pk).aggregate(
        spent_money_year=Sum(
            'price',
            filter=Q(created_date__gte=now - timezone.timedelta(days=365))
        ),
        tickets_last_year=Count(
            'id',
            filter=Q(created_date__gte=now - timezone.timedelta(days=365))
        ),
        spent_money_month=Sum(
            'price',
            filter=Q(created_date__gte=now - timezone.timedelta(weeks=4)
                     )),
        tickets_last_month=Count(
            'id',
            filter=Q(created_date__gte=now - timezone.timedelta(weeks=4))
        ),
        spent_money_week=Sum(
            'price',
            filter=Q(created_date__gte=now - timezone.timedelta(days=7))
        ),
        tickets_last_week=Count(
            'id',
            filter=Q(created_date__gte=now - timezone.timedelta(days=7))
        )
    )
    return render(request, 'pages/ecommerce/index.html', context={**user_orders_info})


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
    search_word = request.GET.get('q')

    tickets = Ticket.objects.filter(status=TicketStatus.available)
    if search_word:
        tickets = tickets.filter(name__contains=search_word)

    page = request.GET.get('page', 1)

    paginator = Paginator(tickets, 2)

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    return render(request, 'pages/ecommerce/tickets.html', context={'tickets': tickets})
