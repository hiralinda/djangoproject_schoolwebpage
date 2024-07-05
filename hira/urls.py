from django.urls import path
from .views import index, home
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('student_home/', views.student_home, name='student_home'),
    # path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    # path('profile/', views.profile, name='profile'),
    path('profile<int:user_id>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('browse_teachers/', views.browse_teachers, name='browse_teachers'),  # Browse teachers
    path('inbox/', views.inbox, name='inbox'),  # Inbox
]