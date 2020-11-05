from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, phone, city,  password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not phone:
            raise ValueError(_('Users must have a Phone Number'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            city=city,

        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, city,  password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            city=city,


            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone = models.CharField(max_length=12, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'city']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)


class Destination(models.Model):
    dname = models.CharField(max_length=255)
    dstate = models.CharField(max_length=255)
    info = models.TextField()

    def __str__(self):
        return self.dname

    def popular_spots(self):
        return self.popularspots_set_values_list('pname', flat=True)


class PopularSpots(models.Model):
    d_id = models.ForeignKey(Destination, on_delete=models.CASCADE)
    pname = models.CharField(max_length=255)
    popic = models.ImageField(
        upload_to='pop/%Y/%m/%d/', blank=True, default='media/h.jpg')


class Hotel(models.Model):
    info = models.TextField(blank=True, null=True)
    tier = models.IntegerField()
    hname = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    d_id = models.ForeignKey(Destination, on_delete=models.CASCADE)
    hpic = models.ImageField(
        upload_to='hotel/%Y/%m/%d/', blank=True, default='media/h.jpg')

    def __str__(self):
        return self.hname

    def luxuries(self):
        return self.luxury_set_values_list('name', flat=True)


class Luxury(models.Model):
    hotel = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Mot(models.Model):
    fare = models.FloatField()
    t_type = models.CharField(max_length=20)


class Roadways(models.Model):
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE)
    carname = models.CharField(max_length=30)
    cartype = models.CharField(max_length=20)


class Railways(models.Model):
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE)
    ac_nac = models.CharField(max_length=20)
    c_class = models.CharField(max_length=20)


class Airways(models.Model):
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE)
    foodAC = models.CharField(max_length=20)
    A_class = models.CharField(max_length=20)


class Package(models.Model):
    name = models.CharField(max_length=100)
    days = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    cost = models.FloatField()
    ppic = models.ImageField(
        upload_to='package/%Y/%m/%d/', blank=True, default='media/h.jpg')
    review = models.IntegerField()


class Booking(models.Model):

    n_people = models.IntegerField()
    trip_date = models.DateField()
    total = models.FloatField()
    rooms = models.IntegerField()
    payment_mode = models.CharField(max_length=50)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
