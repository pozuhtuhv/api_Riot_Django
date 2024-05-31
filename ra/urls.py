from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('ra/', include('ra.urls'))
]
