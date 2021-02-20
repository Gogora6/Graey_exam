from django.urls import path

from .views import user_login, user_logout, user_registration

app_name = 'user'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_registration, name='register'),

]
