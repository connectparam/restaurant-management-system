from django.contrib import admin
from .models import MenuItem,Order,OrderItem,TableBooking

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(TableBooking)
