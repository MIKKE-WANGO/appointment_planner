from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('products/', views.products, name='products'),

    #path('create_order/', views.createorder, name='create_order'),
    path('create_order/<str:pk>/', views.createorder, name='create_order'),
    path('update_order/<str:pk>/', views.updateorder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteorder, name='delete_order'),
]
