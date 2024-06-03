from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from ra.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ra/', include('ra.urls')),
]

handler404 = custom_404