from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateitem,name='updateitem'),
    path('process_order',views.processOrder,name='processOrder'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("contact/",views.contact,name='contact'),
    path("about/",views.about,name='about'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]