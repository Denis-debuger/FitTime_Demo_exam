from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('trainings/', views.trainings, name='trainings'),
    path('booking/', views.booking_create, name='booking_create'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel/<int:pk>/status/', views.change_status, name='change_status'),
]
