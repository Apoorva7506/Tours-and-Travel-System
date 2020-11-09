from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import auth
from django.contrib import messages
import re
from .choices import *


def index(request):
    u = request.user
    p = Package.objects.all().order_by('-review')[:6]
    d = Destination.objects.all()
    s = []
    for j in d:
        if j.dstate not in s:
            s.append(j.dstate)

    context = {
        'p': p,
        'd': d,
        's': s,
        'c': cost_c,
        't': tier_c,
        'm': mot_c,
        'days': days_c,
        'u': u,
    }

    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        city = request.POST['city']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('index')
        elif(not re.search(regex, email)):
            messages.info(request, "Invalid Email")
            return redirect('index')
        elif(len(phone) < 9 or len(phone) > 10):
            messages.info(request, "Invalid Phone Number")
            return redirect('index')
        elif(not phone.isdecimal()):
            messages.info(request, "Invalid Phone Number")
            return redirect('index')

        else:

            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            email=email, phone=phone, city=city, password=password)
            user.save()
            messages.info(request, "You are now registered")
            return redirect('index')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, "Logged in successfully")
            return redirect('index')
        else:
            messages.info(request, "Invalid Credentials,Try Again")
            return redirect('index')


def edit(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        user = User.objects.get(email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.save()
        messages.info(request, "Details Changed")
        return redirect('index')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)

        messages.info(request, "Logged Out Successfully")
        return redirect('index')


def booking(request, p_id):
    p = Package.objects.get(pk=p_id)
    return render(request, 'booking.html', {'u': request.user, 'p': p})


def browse(request):
    p = Package.objects.all()
    d = Destination.objects.all()
    s = []
    for j in d:
        if j.dstate not in s:
            s.append(j.dstate)

    context = {
        'u': request.user,
        'p': p,
        'd': d,
        's': s,
        'c': cost_c,
        't': tier_c,
        'm': mot_c,
        'days': days_c
    }
    return render(request, 'browse.html', context)


def search(request):
    if request.user.is_authenticated:
        p = Package.objects.all()

        if 'state' in request.GET:
            state = request.GET['state']
            if state != "Any":
                p = p.filter(destination__dstate=state)

        if 'dest' in request.GET:
            dest = request.GET['dest']
            if dest != "Any":
                p = p.filter(destination__dname=dest)

        if 'tier' in request.GET:
            tier = request.GET['tier']
            if tier != "Any":
                p = p.filter(hotel__tier=tier)

        if 'mot' in request.GET:
            mot = request.GET['mot']
            if mot != "Any":
                p = p.filter(mot__t_type=mot)

        if 'cost' in request.GET:
            cost = request.GET['cost']
            if cost != "Any":
                p = p.filter(cost__lte=int(cost))

        if 'days' in request.GET:
            days = request.GET['days']
            if days != "Any":
                p = p.filter(days=int(days))

        d = Destination.objects.all()
        s = []
        for j in d:
            if j.dstate not in s:
                s.append(j.dstate)

        context = {
            'p': p,
            'd': d,
            's': s,
            'c': cost_c,
            't': tier_c,
            'm': mot_c,
            'days': days_c,
            'v': request.GET
        }
        return render(request, 'browse2.html', context)
    else:
        messages.info(request, "Login Required")
        return redirect('index')


def package(request, p_id):
    if request.user.is_authenticated:
        p = Package.objects.get(pk=p_id)
        pop = PopularSpots.objects.filter(d_id=p.destination)
        lux = Luxury.objects.filter(hotel=p.hotel)
        return render(request, 'package.html', {'u': request.user, 'p': p, 'pop': pop, 'lux': lux})
    else:
        messages.info(request, "Login Required")
        return redirect('index')


def book(request, p_id):
    p = Package.objects.get(pk=p_id)
    u = request.user
    checkin = request.GET['check_in']
    ppl = request.GET['pass']
    food = request.GET['food']
    rooms = request.GET['rooms']
    pay = request.GET['pay']

    if(u == '' or rooms == '' or ppl == '' or pay == 'Any' or food == 'Any'):
        messages.info(request, "Please fill the form properly")
        return render(request, 'booking.html', {'p': p})
    else:
        tcost = p.cost*int(ppl)
        tcost = tcost+p.mot.fare*int(ppl)
        r = int(int(ppl)/2)
        r1 = int(rooms)-r
        if(r1 > 0):
            tcost = tcost+tcost*0.2*r1
        if(food == "Yes"):
            tcost = tcost+tcost*0.2
        b = Booking(trip_date=checkin, n_people=ppl, total=tcost,
                    payment_mode=pay, rooms=int(rooms), package=p, customer=u)
        b.save()
        messages.info(request, "Booking Successful\n Total is Rs." +
                      str(b.total)+"\n Thank You!")
        return redirect('index')


def booked(request):
    u = request.user
    b = Booking.objects.filter(customer=u).order_by('-trip_date')
    context = {
        'b': b,
        'u': u
    }
    return render(request, 'booked.html', context)
