from django.urls import path
from .views import index, home_view
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('home/', home_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('student_home/', views.student_home, name='student_home'),
]