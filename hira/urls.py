from django.urls import path
from .views import index, home_view

urlpatterns = [
    path('', index, name='index'),
    path('home/', home_view, name='home'),
]