from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import *
from .utils import cookieCart, cartData, guestOrder
import json
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    categories = Product.objects.values('category').distinct()
    all_products = []
    for category in categories:
        products = Product.objects.filter(category=category['category'])
        all_products.append({'category': category['category'], 'products': products})
    context = {"all_products": all_products,'cartItems':cartItems}
    return render(request,'stores/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'stores/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'stores/checkout.html',context )

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        if orderItem.quantity == 0:
            orderItem.delete()

    if orderItem.quantity == 0:
        orderItem.delete()
    else:
        orderItem.save()

    if order.get_cart_items == 0:
        order.delete()
    return JsonResponse("item added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('payment complete', safe=False)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'stores/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'stores/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def contact(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'stores/contact.html')

def about(request):
    return render(request, 'stores/about.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'stores/product_detail.html', context)
