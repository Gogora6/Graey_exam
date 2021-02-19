from django.urls import path

from .views import index, create_orders, orders_list, ticket_list

app_name = 'ecommerce'
urlpatterns = [
    path('', index, name='index'),
    path('create/orders/', create_orders, name='create_orders'),
    path('orders', orders_list, name='orders_list'),
    path('tickets', ticket_list, name='tickets_list'),

]
