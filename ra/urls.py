from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 기본 페이지
    path('match_info/<str:username>/<str:tag>/', views.get_match_info, name='get_match_info'),
]