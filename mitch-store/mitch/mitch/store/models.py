from django.db import models
from django.contrib.auth.models import  User
from django.urls.base import reverse
# Create your models here

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    name = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField( max_length=100, null=True,blank=True)
    mobile_number = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,blank=True)
    price = models.DecimalField(max_digits= 7, decimal_places=2,blank=True)
    category_choices = [
        ("Bags", "Bags"),
        ("Bag straps", "Bag straps"),
        ("Headbands", "Headbands"),
        ("Headwraps","Headwraps"),
        ("Turban Hats", "Turban Hats"),
        ("Dog harnesss", "Dog harness"),
        ("Dog leash", "Dog leash"),
        ("Other", "Other")
    ]
    other = "Other"
    category = models.CharField(max_length=200,null=True, choices=category_choices, default=other)
    description = models.TextField(null=True,blank=True)
    date_added = models.DateTimeField(null=True,blank=True)
    image = models.ImageField(null=True ,blank=True)
    image1 = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    @property
    def image1URL(self):
        try:
            url = self.image1.url
        except:
            url =''
        return url
    
    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url =''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return str(self.id)

    #total price
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    #total quantity
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    made = models.BooleanField(default=False)
    def __str__(self):
        return self.product.name


    @property
    def get_total(self):
        total = self.product.price *self.quantity
        return total


#Mpesa models
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# M-pesa Payment models
#store mpesa calls
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'

#stores accepted transactions
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'

#store succesful transactions
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name