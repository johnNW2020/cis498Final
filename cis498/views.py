from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.contrib import messages

from cis498.forms import SignUpForm, MenuForm, CheckoutForm
from cis498.mongodb.customers import Customers
from cis498.mongodb.drivers import Drivers
from cis498.mongodb.menu import Menu
from cis498.mongodb.cart import Cart

from cis498.mongodb.orders import Orders


@login_required()
def home(request):
    menu = get_menu()
    order = get_order(request)
    total = get_total(order)
    context = {
        'menu': menu,
        'order': order,
        'total': total
    }
    return render(request, 'home.html', context)


@staff_member_required()
def staffhome(request):
    order = Orders()
    orders = order.getCurrentOrders()

    context = {
        'orders': orders
    }
    return render(request, 'staffhome.html', context)


@login_required()
def checkout(request):
    if request.POST:
        form = CheckoutForm(request.POST)
        cart = get_order(request)
        cartItems = []
        for items in cart:
            cartItems.append(items['name'])
        order = Orders()
        order.generateOrder(request.user, cartItems, form)
        delete_cart_order(request.user.email)
        return redirect(ordertracker)
    else:
        order = get_order(request)
        total = get_total(order)
        form = CheckoutForm()
        context = {
            'form': form,
            "total": total,
            "order": order
        }
        return render(request, 'checkout.html',  context)


@login_required()
def ordertracker(request):
    cust = Customers()
    customer = cust.findCustomerByEmail(request.user.email)
    order = Orders()
    orders = order.getCurrentUserOrder(request.user.email, customer)
    context = {
        'order': orders
    }
    return render(request, 'ordertracker.html', context)


@staff_member_required()
def driverhome(request):
    order = Orders()
    orders = order.get_driver_orders(request.user.username)
    context = {
        'orders': orders
    }
    return render(request, 'driverhome.html', context)


@login_required()
def add_to_cart(request, **kwargs):
    user = request.user
    cart = Cart()
    item_id = kwargs.get('item_id', "")
    menu = Menu()
    item = menu.findById(item_id)
    cart_item = {
        "name": item.name,
        "price": item.price,
        "item_id": item_id
    }
    if cart.doesOrderExist(user.email):
        cart.addToCart(user.email, cart_item)
    else:
        cart.createCartItem(user.email, cart_item)

    messages.info(request, "item added to cart")
    return redirect(reverse('home'))


@login_required()
def delete_from_cart(request, **kwargs):
    email = request.user.email
    cart = Cart()
    item_id = kwargs.get('item_id')
    cart.deleteItemFromCart(email, item_id)
    return redirect(reverse('home'))


@staff_member_required()
def updateOrders(request, **kwargs):
    order = kwargs.get('item_id')
    orders = Orders()
    orders.updateOrder(order)
    return redirect('staffhome')


@staff_member_required()
def updateDriverOrders(request, **kwargs):
    order = kwargs.get('item_id')
    orders = Orders()
    orders.updateOrder(order)
    return redirect('driverhome')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            create_account(form)
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            request.session['username'] = username
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def stafflogin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and not is_driver(username):
                login(request, user)
                return redirect('staffhome')
            elif user.is_active and is_driver(username):
                login(request, user)
                return redirect('driverhome')
    return render(request, 'stafflogin.html')


def is_driver(email):
    driver = Drivers()
    return driver.is_driver(email)


def create_account(form):
    customer = Customers()
    customer.createCustomer(form)


def create_menu_item(form):
    menu = Menu()
    menu.createNewItem(form)


def update_menu_item(form):
    menu = Menu()
    menu.updateMenuItem(form)


@staff_member_required()
def editMenuItem(request):
    m = Menu()
    menu = m.menuNames()
    context = {
        'results': menu
    }
    if request.POST:

        form = MenuForm(request.POST)
        id = form['item_id']
        if form.is_valid():
            if id.data == 'EMPTY':
                create_menu_item(form)
            else:
                update_menu_item(form)
            return redirect('staffhome')
    elif request.GET:
        if request.GET['menuitems'] == 'Add Item':
            form = MenuForm(initial={'item_id':'EMPTY'})
        else:
            form = findAndEditMenuItem(request)
        context['form'] = form
        return render(request, 'staffeditmenu.html', context)

    return render(request, 'staffeditmenu.html', context)


def findAndEditMenuItem(request):
    m = Menu()
    pizza = m.findByName(request.GET['menuitems'])
    form = MenuForm(initial={'name': pizza.name, 'type': pizza.type, 'price': pizza.price,
                                     'description': pizza.description, 'item_id':pizza.id})
    return form


def get_menu():
    menu = Menu()
    return menu.pizza()


def get_order(request):
    cart = Cart()
    return cart.cartItems(request.user.email)

def get_order_id(request):
    cart = Cart()
    cartOrder = cart.getCartOrder(request.user.email)
    return cartOrder.id


def get_total(order):
    total = 0.0
    if order:
        for item in order:
            total += float(item['price'])
        total = "{:10.2f}".format(total * 1.0625)
    return total

def delete_cart_order(email):
    cart = Cart()
    cart.deleteCart(email)
