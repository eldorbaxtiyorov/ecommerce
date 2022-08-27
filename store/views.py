from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def store(request):
    if request and request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    products = Product.objects.all()
    context = {'products': products, 'order': order}
    return render(request, 'store/store.html', context)


def login(request):
    # print(111111111111111111111111111111111111111111111111111111111111, request.GET['fname'][0])
    # print(222222222222222222222222222222222222222222222222222222222222, 'lname' in request and 'fpassword' in request)
    # def get(request):
    #     name = request.GET['fname'][0]
    #     password = request.GET['lpassword'][0]
    #     print(name, password)
    #     if authenticate(username=name, password=password) is not None:
    #         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #         # return render(request, 'store/login.html')
    #     else:
    #         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # def f(request):
    #     return render(request, 'store/login.html')

    pass
# No backend authenticated the credentials


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order, }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    print(request)
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
