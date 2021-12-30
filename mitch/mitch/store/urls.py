
from django.urls import path
from . import views

urlpatterns = [
    path(r'^category/(?P<str:category>\w+)/$', views.category, name= 'category'), 
    path('category/', views.category, name= 'category'), 
    path(r'^product/(?P<int:id>\d+)/$', views.product, name= 'product'),
    path('product/', views.product, name= 'product'), 
    path('shop/', views.shop, name= 'shop'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('', views.home, name='home'),
    path('process_order/' ,views.processOrder,name='process_order'),
    path('update_item/', views.updateItem, name='update_item'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    #path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    #path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    #register, confirmation, validation and callback urls
    #path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    #path('c2b/confirmation', views.confirmation, name="confirmation"),
    #path('c2b/validation', views.validation, name="validation"),
    #path('c2b/callback', views.call_back, name="call_back"),

]
