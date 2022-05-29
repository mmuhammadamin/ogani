import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from apps.products.models import Product


class WishList(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    product=models.ManyToManyField(Product)

    def __str__(self):
        return f'wishist of {self.user.username}'
class Cart(models.Model):
    client=models.OneToOneField(User,on_delete=models.CASCADE)
    cart_total_price=models.FloatField(null=True)

    @property
    def get_cart_items(self):
        cart_items=self.cart_items.all()
        total=sum([item.quantity for item in cart_items])
        return total
    
    @property
    def get_cart_total(self):
        cart_items=self.cart_items.all()
        total=sum([item.total for item in cart_items])
        return total
    def __str__(self):
        return f'order of {self.client}'



class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True,related_name='cart_item')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(null=True)
    total=models.FloatField(null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    STATUS=(
        (0,'NEW'),
        (1,'PROCESS'),
        (2,'DELIVERED'),
        (3,'CANCELLED'),
    )
    transaction_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    cart=models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    client=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    phone=models.CharField(max_length=122)
    address=models.CharField(max_length=222)
    note=models.TextField(null=True,blank=True)
    order_total_price=models.FloatField(null=True)
    status=models.IntegerField(choices=STATUS,default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order of {self.client}| {self.transaction_id}'

def cart_item_post_save(sender,instance,created,*args,**kwargs):
    if created:
        total_price=instance.quantity*instance.product.price
        instance.total=total_price
        instance.save()
post_save.connect(cart_item_post_save,sender=CartItem)