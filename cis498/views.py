from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, CreateView

from cis498.forms import SignUpForm, MenuForm
from cis498.models import MenuModel
from cis498.mongodb.customers import Customers
from cis498.mongodb.menu import Menu

from cis498.mongodb.orders import Orders


@login_required()
def home(request):
    m = Menu()
    men = m.pizza()
    context = {
        'menu': men
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
    return render(request, 'checkout.html')

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

@login_required()
def checkout(request):
    return render(request, 'checkout.html')

@login_required()
def driverhome(request):
    return render(request, 'driverhome.html')

@login_required()
def addtocart(request, **kwargs):
    user = request.user
    menu = Menu()
    item = menu.findById(id=kwargs.get('item_id', ""))
    order = Orders()
    order.generateOrder(user, item, '')
    return redirect('home')

@staff_member_required()
def updateOrders(request, **kwargs):
    order = kwargs.get('item_id')
    orders = Orders()
    orders.updateOrder(order)
    return redirect('staffhome')

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
            if user.is_active:
                login(request, user)
                return redirect('staffhome')
    return render(request, 'stafflogin.html')


def create_account(form):
    customer = Customers()
    customer.createCustomer(form)

def create_menu_item(form):
    menu = Menu()
    menu.createNewItem(form)

def update_menu_item(form):
    menu = Menu()
    menu.updateMenuItem(form)

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

