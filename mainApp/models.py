from django.db import models
from datetime import datetime
from django.db.models.fields.related import ForeignKey

class MainCategory(models.Model):
    mcid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Seller(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,null=True,blank=True)
    

    def __str__(self):
        return str(self.sid)+' '+self.name 

class Superuser(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,null=True,blank=True)
    
    
    def __str__(self):
        return str(self.bid)+' '+self.name 
        
class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    pro_code = models.CharField(max_length=10)
    price = models.IntegerField()
    mainCat = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subCat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)        
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,default=None)
    superuser = models.ForeignKey(Superuser,on_delete=models.CASCADE)
    mfcdate = models.DateField(default=datetime.now,blank=True)
    expdate = models.DateField(default=datetime.now,blank=True)
    pro_owner = models.CharField(max_length=50)
    curent_time = models.DateTimeField(auto_now_add=True)
    pic1 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)

    def __str__(self):
        return str(self.pid)+" "+self.name


        

