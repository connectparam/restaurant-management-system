import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem, Order, OrderItem, TableBooking

# -------- MENU ITEM APIs --------

@csrf_exempt
def menu_list(request):
    if request.method == 'GET':
        items = list(MenuItem.objects.values())
        return JsonResponse({'menu_items': items}, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        item = MenuItem.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            available=data.get('available', True)
        )
        return JsonResponse({'id': item.id, 'message': 'Item created'}, status=201)

@csrf_exempt
def menu_detail(request, pk):
    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'available': item.available
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.price = data.get('price', item.price)
        item.available = data.get('available', item.available)
        item.save()
        return JsonResponse({'message': 'Item updated'})

    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'message': 'Item deleted'})

# -------- ORDER APIs --------

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = Order.objects.create(customer_name=data['customer_name'])
        for item in data['items']:
            OrderItem.objects.create(
                order=order,
                menu_item_id=item['menu_item_id'],
                quantity=item['quantity']
            )
        return JsonResponse({'id': order.id, 'message': 'Order created'}, status=201)

def order_list(request):
    if request.method == 'GET':
        orders = []
        for order in Order.objects.all():
            items = list(order.items.values('menu_item__name', 'quantity'))
            orders.append({
                'id': order.id,
                'customer_name': order.customer_name,
                'created_at': order.created_at,
                'items': items
            })
        return JsonResponse({'orders': orders}, safe=False)

# -------- BOOKING APIs --------

@csrf_exempt
def booking_list(request):
    if request.method == 'GET':
        bookings = list(TableBooking.objects.values())
        return JsonResponse({'bookings': bookings}, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        booking = TableBooking.objects.create(
            name=data['name'],
            booking_time=data['booking_time'],
            num_people=data['num_people']
        )
        return JsonResponse({'id': booking.id, 'message': 'Booking created'}, status=201)
