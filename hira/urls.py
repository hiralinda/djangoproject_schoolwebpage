from django.urls import path
from .views import index, home
from . import views

from .views import CustomLoginView

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('browse_teachers/', views.browse_teachers, name='browse_teachers'), 
    path('inbox/', views.inbox, name='inbox'), 
    path('inbox/<int:user_id>/', views.inbox, name='inbox'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('availability/', views.availability_view, name='availability'),
    path('authorize/', views.authorize, name='authorize'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('schedule/', views.schedule_class, name='schedule_class'),
    path('scheduled_classes/', views.scheduled_classes, name='scheduled_classes'),
    

]

