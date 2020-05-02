from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, render_to_response

from cis498.forms import SignUpForm
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
    print(request.method)
    return render(request, 'ordertracker.html')

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
    test = kwargs.get('item_id', "")
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


