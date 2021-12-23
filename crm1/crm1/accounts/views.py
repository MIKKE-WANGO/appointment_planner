from django.db import reset_queries
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory

from .filters import*
from .models import * 
from .forms import*
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count
    pending  = orders.filter(status='Pending').count


    context = {'orders': orders, 'customers':customers, 'delivered':delivered, 'pending':pending , 'total_customers':total_customers, 'total_orders':total_orders }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    
    return render(request, 'accounts/products.html', {'products':products})

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count':order_count, 'myfilter':myfilter}

    return render(request, 'accounts/customers.html', context)


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

def deleteorder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={"item":order}
    return render(request, 'accounts/delete.html', context)