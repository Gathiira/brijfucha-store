from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=100)

	def __str__(self):
		return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=200, null=False)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    product_quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to ='products')
    date_added = models.DateTimeField(auto_now_add=True)
    digital = models.BooleanField(default=False,null=True,blank=False)
    finished = models.BooleanField(default=False,null=True, blank=False)

    def __str__(self):
        return self.product_name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null= True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == True:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.order_quantity for item in orderitems ])
        return total    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    order_quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_quantity)+' '+self.product.product_name

    @property
    def get_total(self):
        total = self.product.price * self.order_quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=False)
    county = models.CharField(max_length=100, null=False)
    town = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address +' ' + self.county +' ' + self.town




