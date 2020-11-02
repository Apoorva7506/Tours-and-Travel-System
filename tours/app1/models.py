from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
            self, email,username,fname,mname,lname, phone,age, houseno,city,state, password=None, commit=True):
        if not email:
            raise ValueError(('Users must have an email address'))
        if not username:
            raise ValueError(('Users must have a username'))
        if not fname:
            raise ValueError(('Users must have a first name'))
        if not mname:
            raise ValueError(('Users must have a middle name'))
        if not nname:
            raise ValueError(('Users must have a last name'))
        if not phone:
            raise ValueError(('Users must have a phone number'))
        if not age:
            raise ValueError(('Users must have an age'))
        if not houseno:
            raise ValueError(('Users must have a houseno'))
        if not city:
            raise ValueError(('Users must have a city'))    
        if not state:
            raise ValueError(('Users must have a state'))

        user = self.model(
            email=self.normalize_email(email),
            fname=fname,
            mname=mname,
            lname=lname,
            username=username,
            age=age,
            houseno=houseno,
            city=city,
            state=state,
            phone=phone,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fname,mname,lname, phone, password , age, houseno,city,state):
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            mname=mname,
            lname=lname,
            username=username,
            age=age,
            houseno=houseno,
            city=city,
            state=state,
            phone=phone,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=('email address'), max_length=255, unique=True)
    username = models.CharField(('username'), max_length=100, blank=True, unique=True)
    phone = models.CharField(max_length=10)
    fname=models.CharField(('fname'),max_length=255)
    mname=models.CharField(('mname'),max_length=255)
    lname=models.CharField(('lname'),max_length=255)
    age=models.IntegerField()
    houseno=models.CharField(('houseno'),max_length=255)
    city=models.CharField(('city'),max_length=255)
    state=models.CharField(('state'),max_length=255)
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )

    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        ('date joined'), default=datetime.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state']

    def __str__(self):
        return(self.username)

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


class CustomerNumber(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    cnumber=models.IntegerField()


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
    tier=models.IntegerField()
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


class Package(models.Model):
    days=models.IntegerField()
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    mot=models.ForeignKey(Mot,on_delete=models.CASCADE)
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    cost=models.FloatField()

class Booking(models.Model):
    n_people=models.IntegerField()
    trip_date=models.DateField()
    total=models.FloatField()
    rooms=models.IntegerField()
    payment_mode=models.CharField(max_length=50)
    package=models.ForeignKey(Package,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)