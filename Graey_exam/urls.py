from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')),
    path('', include('ecommerce.urls'))
]

