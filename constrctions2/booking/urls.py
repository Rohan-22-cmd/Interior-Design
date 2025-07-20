# urls.py

from django.urls import path
from .views import admin_dashboard1, booking_now, booking_submit
app_name = 'booking'
urlpatterns = [
    path('booking-now/', booking_now, name='booking_now'),
    path('booking-submit/', booking_submit, name='booking_submit'),
    path('admin-dashboard/',admin_dashboard1, name='admin_dashboard'),  
]
