from django.urls import path
from . import views

urlpatterns = [
    # Menu APIs
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),

    # Order APIs
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),

    # Booking APIs
    path('bookings/', views.booking_list, name='booking_list'),
]
