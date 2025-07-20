from django.urls import path
from . import views

urlpatterns = [
    path('project_list/', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_details, name='project_details'),
    path('home1/', views.home1_view, name='home1'),
    path('', views.home2_view, name='home2'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('informatin/', views.informatin_you_view, name='informatin'),
    path('consultation/', views.book_consultation, name='book_consultation'),
]