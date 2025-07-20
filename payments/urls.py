from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-payment/', views.generate_payment, name='generate_payment'),
    path('verify-payment/', views.verify_payment_status, name='verify_payment'),
    path('webhook/', views.webhook, name='webhook'),
   
]