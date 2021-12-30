import json


#add functionality to check if client id on backend is equal to client id on the front end


#needed for forms
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 

from django.http import JsonResponse, request
from .filters import*
from .models import * 
import datetime
from .utils import cookieCart, cartData, guestOrder
from .forms import NewUserForm
from django.urls import reverse
#enable password reset and sending an email throught view function
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

#enable mpesa 
import requests
from requests.auth import HTTPBasicAuth
#from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#MPesa view that generates mpesa token
#def getAccessToken(request):
   # consumer_key = 'kP71O9Bt2ilvossCR1uGU5eC1Bhg4k9q'
    #consumer_secret = 'cqc0AOccsoXTikGZ'
    #api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    #r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    #mpesa_access_token = json.loads(r.text)
    #validated_mpesa_access_token = mpesa_access_token['access_token']
    #return HttpResponse(validated_mpesa_access_token)

#stk push method
#def lipa_na_mpesa_online(request):
    #access_token = MpesaAccessToken.validated_mpesa_access_token
    #api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    #headers = {"Authorization": "Bearer %s" % access_token}
    #request = {
        #"BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        #"Password": LipanaMpesaPpassword.decode_password,
        #"Timestamp": LipanaMpesaPpassword.lipa_time,
        #"TransactionType": "CustomerPayBillOnline",
        #"Amount": 1,
        #"PartyA": 254746460915,  # number sending money,replace with your phone number to get stk push
        #"PartyB": LipanaMpesaPpassword.Business_short_code,
        #"PhoneNumber": 254746460915,  #number receiving stk push, replace with your phone number to get stk push
        #"CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        #"AccountReference": "Henry",
        #"TransactionDesc": "Testing stk push"
    #}
    #response = requests.post(api_url, json=request, headers=headers)
    #return HttpResponse('success')

#register our confirmation and validation URL with Safaricom.
##@csrf_exempt
#def register_urls(request):
    #access_token = MpesaAccessToken.validated_mpesa_access_token
    #api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    #headers = {"Authorization": "Bearer %s" % access_token}
    #options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               #"ResponseType": "Completed",
               #"ConfirmationURL": "  https://57f2-154-123-198-111.ngrok.io/c2b/confirmation",
               #"ValidationURL": "  https://57f2-154-123-198-111.ngrok.io/c2b/validation"}
    #response = requests.post(api_url, json=options, headers=headers)
    #return HttpResponse(response.text)

#@csrf_exempt
#def call_back(request):
    #pass

# accept the payment by responding with ResultCode: 0 and ResultDesc: Accepted. Note if change 0 to any other number, you reject the payment.
#@csrf_exempt
#def validation(request):
    #context = {
        #"ResultCode": 0,
        #"ResultDesc": "Accepted"
   # }
   # return JsonResponse(dict(context))

#ave successfully transaction in our database.  
#@csrf_exempt
#def confirmation(request):
   # mpesa_body =request.body.decode('utf-8')
   # mpesa_payment = json.loads(mpesa_body)
   # payment = MpesaPayment(
   #     first_name=mpesa_payment['FirstName'],
   #     last_name=mpesa_payment['LastName'],
   #     middle_name=mpesa_payment['MiddleName'],
   #     description=mpesa_payment['TransID'],
    #    phone_number=mpesa_payment['MSISDN'],
     #   amount=mpesa_payment['TransAmount'],
      #  reference=mpesa_payment['BillRefNumber'],
       # organization_balance=mpesa_payment['OrgAccountBalance'],
        #type=mpesa_payment['TransactionType'],
    #)
    #payment.save()
    #context = {
     #   "ResultCode": 0,
      #  "ResultDesc": "Accepted"
    #}
    #return JsonResponse(dict(context))


#reset password view
#During production, the domain, site name, protocol, and from email address will need to be changed. 
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "store/password/email_reset.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="store/password/password_reset.html", context={"password_reset_form":password_reset_form})



#register form
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            
			
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="store/register.html", context={"form":form})

#login form
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="store/login.html", context={"login_form":form})

#logout
def logout_request(request):
	logout(request)
	messages.success(request, "You have successfully logged out.") 
	return redirect("home")

#view categories
def category(request,category):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(category=category)
    context = {'products':products, 'cartItems':cartItems}

   
    return render(request, 'store/category.html',context)



#view product 
def product(request,id):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
   
    product = Product.objects.get(pk=id)
    context = {'product':product, 'cartItems':cartItems}

   
    return render(request, 'store/product.html',context)


def shop(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
         
    products = Product.objects.all()
    myfilter = CategoryFilter(request.GET, queryset=products)
    products = myfilter.qs

    context = {'products':products, 'cartItems':cartItems,'myfilter':myfilter}
    return render(request, 'store/shop.html',context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order,'cartItems':cartItems}
    
    return render(request, 'store/checkout.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order,'cartItems':cartItems}
    
    return render(request, 'store/cart.html', context)

def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems':cartItems}
    return render(request, 'store/home.html',context)


#adds or removes items to cart 
def updateItem(request):
    #loads data sent from fetch function in js
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, paid=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
   
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#process payment and update database
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, paid=False)

        
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.paid = True
    order.save()

    return JsonResponse('Payment submitted',safe=False)