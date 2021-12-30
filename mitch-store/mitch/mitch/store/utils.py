import datetime
import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}

    print(cart)
    items =[]
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    #loop through cart items stored in the cart cookie
    for i in cart:
        try:
            #updates cart total
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            #updates cart total
            order['get_cart_total'] += total
            #updates cart quantity
            order['get_cart_items'] += cart[i]['quantity']

            #creating a product and its attributes
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }

            items.append(item)
        except:
            pass

    return{'items': items, 'order': order,'cartItems':cartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email )
        

        customer = request.user.customer

        
        order, created = Order.objects.get_or_create(customer=customer, paid=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

        

    return{'items': items, 'order': order,'cartItems':cartItems}


def guestOrder(request,data): 
    print('user is not logged in')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    tel = data['form']['tel']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name= name
    customer.mobile_number= tel
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete=False,
        paid = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        ) 

    return customer, order

