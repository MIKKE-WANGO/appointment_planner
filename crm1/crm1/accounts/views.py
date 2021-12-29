from django.db import reset_queries
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, logout,login
from .filters import*
from .models import * 
from .forms import*
from .decorators import*
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin','customer'])
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count
    pending  = orders.filter(status='Pending').count
    

    context = {'orders': orders, 'customers':customers, 'delivered':delivered, 'pending':pending , 'total_customers':total_customers, 'total_orders':total_orders }
    return render(request, 'accounts/dashboard.html', context)

@admin_only
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    
    return render(request, 'accounts/products.html', {'products':products})

@admin_only
@login_required(login_url='login')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count':order_count, 'myfilter':myfilter}

    return render(request, 'accounts/customers.html', context)

@admin_only
@login_required(login_url='login')
def createorder(request,pk):

    #takes parent model and child model and specify whicj=h fields for child product
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer) 
    #form = OrderForm(initial={'customer':customer})
    if request.method=='POST':
        #save form details
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer) 
        if formset.is_valid():
            formset.save() 
            return redirect('/')

    context = {'formset': formset }
    return render (request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateorder(request,pk):

    #get a form filled with a specific order's details
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    #save form details
    # 'instance= order' prevents it from creating a new order
    if request.method=='POST':
        form = OrderForm(request.POST, instance= order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render (request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={"item":order}
    return render(request, 'accounts/delete.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Username or passowrd is incorrect')
    context ={}
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group) 
            Customer.objects.create(user=user,name=user.username,email=user.email)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')


    context ={'form': form}
    return render(request, 'accounts/register.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count
    pending  = orders.filter(status='Pending').count
    
    context ={'orders':orders,'delivered':delivered, 'pending':pending , 'total_orders':total_orders} 
    return render(request, 'accounts/user.html', context)


def accountsettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()

    context= {'form':form}
    return render(request, 'accounts/settings.html', context)
