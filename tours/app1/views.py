from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import auth
from django.contrib import messages

def index(request):
    return render(request, 'package.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        city = request.POST['city']

        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('index')
 
        else:

            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            email=email, phone=phone, city=city, password=password)
            user.save()
            messages.info(request,"You are now registered")
            return redirect('index')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request,"Logged in successfully")
            return redirect('index')
        else:
            messages.info(request,"Invalid Credentials,Try Again")
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
        messages.info(request,"Details Changed")
        return redirect('index')

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')
 
def book(request):
    if request.method == 'POST':
        if request.POST['check_in'] == '' or request.POST["pass"] == " No. of Passengers " or request.POST["rooms"] == " Rooms " or request.POST["food"] == " Food " or request.POST["pay"]==" Payment Mode ":
            messages.info(request,"Please provide valid details")
            return redirect('index')
        else:
            messages.info(request,"Booking Successful")
            return redirect('index')

