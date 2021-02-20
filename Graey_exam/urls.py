from django.urls import path, include
from django.contrib import admin

app_name = 'main'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('', include('ecommerce.urls'))
]
