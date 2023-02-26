from unicodedata import decimal
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
#class User(models.Model):
#    name=models.CharField(max_length=100)
#    position=models.CharField(max_length=100)
#    password=models.CharField(max_length=10000)

class DrugType(models.Model):
    '''eg: anitbiotic,antimalari,cough mixture'''
    name=models.CharField(max_length=100)
    forms=models.CharField(max_length=10000,blank=True)

class Product(models.Model):
    drug_type=models.ForeignKey(DrugType,on_delete=models.SET_NULL,null=True,blank=True)
    product_name=models.CharField(max_length=70)
    brand_name=models.CharField(max_length=100)
    location=models.CharField(max_length=50,blank=True)  
    description=models.CharField(max_length=200,blank=True)
    sale_form=models.CharField(max_length=100)
    unit_quantity=models.FloatField(default=0)
    package_quantity=models.FloatField(default=0)
    stock_quantity=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self) -> str:
        return self.product_name +' ({})'.format(self.stock_quantity)
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})
    def natural_key(self):
        return (self.product_name,self.brand_name,self.price)

   
class StockedItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    #100 tablets, 64 bottles
    unit_quantity=models.FloatField(default=0)
    #50 12-pac cipro ,etc
    package_quantity=models.FloatField(default=0)
    batch=models.CharField(max_length=100,blank=True)
    package_price=models.DecimalField(default=0, max_digits=19, decimal_places=2)
    unit_price=models.DecimalField(default=0,max_digits=19, decimal_places=2)
    location=models.CharField(max_length=50,blank=True)  
    date=models.DateField(auto_now=True)
    def __str__(self) -> str:
        product=self.product
        return product.product_name+'({})'.format(self.unit_quantity) 
class StockEntry(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT,null=True)
    person=models.ForeignKey(User,on_delete=models.PROTECT)
    date=models.DateTimeField(auto_now_add=True)
    stock_quantity=models.IntegerField(verbose_name='New stock quantity',default=0)
    #package_quantity=models.FloatField(default=0)
    comments=models.CharField(max_length=200,blank=True,null=True)
    supplier=models.ForeignKey('Supplier',on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        ordering=['-date']
    def __str__(self) -> str:
        stocked_item=self.product
        #product=stocked_item.product
        return stocked_item.product_name+' ({} units {} pks)'.format(self.unit_quantity,self.package_quantity)
class Supplier(models.Model):
    company=models.CharField(max_length=200)
    phone=models.CharField(max_length=50)
    contact_person=models.CharField(max_length=200)
    address=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.company

class Customer(models.Model):
    name=models.CharField(max_length=100)
    birth_date=models.DateField(null=True,blank=True, verbose_name="Birth date (YYYY-MM-DD)")
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    identity=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return '{} ({})'.format(self.name ,self.phone)


class SoldItem(models.Model):
    #day=models.IntegerField()
    #month=models.IntegerField()
    #year=models.IntegerField()
    product=models.ForeignKey(StockedItem,on_delete=models.PROTECT)
    vendor=models.ForeignKey(User,on_delete=models.PROTECT)
    stime=models.DateTimeField(auto_now=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2)
    package_quantity=models.FloatField(blank=True)
    unit_quantity=models.FloatField(blank=True)
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,blank=True)
    def __str__(self):
        product=self.product
        return product.product_name
class Sale(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    unit_price=models.DecimalField(decimal_places=2,max_digits=7)
    quantity=models.IntegerField()
    amount=models.DecimalField(decimal_places=2,max_digits=8)
    date=models.DateTimeField(auto_now_add=True)
    sales_record=models.ForeignKey('Sales',on_delete=models.PROTECT,null=True)
class Sales(models.Model):
    amount=models.DecimalField(decimal_places=2,max_digits=9)
    date=models.DateTimeField(auto_now_add=True)
    contact_person=models.ForeignKey(User,on_delete=models.PROTECT) 
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,null=True,blank=True)
    class Meta:
        ordering=['-date']

    