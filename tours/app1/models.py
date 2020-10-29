from django.db import models

# Create your models here.
class Customer(models.Model):
    
    fname=models.CharField(max_length=255)
    mname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    age=models.IntegerField()
    houseno=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    def __str__(self):
        return self.fname
    def customer_number(self):
        return self.customernumber_set_values_list('cnumber',flat=True)


class CustomerNumber(model.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    cnumber=models.IntegerField(max_length=10)


class Destination(models.Model):
    dname=models.CharField(max_length=255)
    dstate=models.CharField(max_length=255)
    def __str__(self):
        return self.dname
    def popular_spots(self):
        return self.popularspots_set_values_list('pname',flat=True)


class PopularSpots(models.Model):
    did=models.ForeignKey(Destination,on_delete=models.CASCADE)
    pname=models.CharField(max_length=255)


class Hotel(models.Model):
    tier=models.IntegerField(max_length=1)
    hname=models.CharField(max_length=255)
    street=models.CharField(max_length=255)
    locality=models.CharField(max_length=255)
    d_id=models.ForeignKey(Destination,on_delete=models.CASCADE)
    def __str__(self):
        return self.hname
    def luxuries(self):
        return self.luxury_set_values_list('name',flat=True)


class Luxury(models.Model):
    hotel= models.ForeignKey(Destination,on_delete=models.CASCADE)
    name= models.CharField(max_length=255)


class Mot(models.Model):
    fare=models.FloatField()
    t_type=models.CharField(max_length=20)

class Roadways(models.Model):
    mot=models.ForeignKey(Mot,on_delete=models.CASCADE)
    carname=models.CharField(max_length=30)
    cartype=models.CharField(max_length=20)

class Railways(models.Model):
    mot=models.ForeignKey(Mot,on_delete=models.CASCADE)
    AC_NAC=models.CharField(max_length=20)
    C_class=models.CharField(max_length=20)


class Airways(models.Model):
    mot=models.ForeignKey(Mot,on_delete=models.CASCADE)
    foodAC=models.CharField(max_length=20)
    A_class=models.CharField(max_length=20)