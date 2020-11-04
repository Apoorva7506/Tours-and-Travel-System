from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        if User.objects.filter(email=email).exists():
            return HttpResponse("<center><h1>Email already exists<br>" + '<a href="/">Click to go back to Index</a></center></h1>')

        else:

            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            email=email, phone=phone, city=None, age=None, password=password)
            user.save()
            html = "<h1><center>You are now registered<br>" + \
                '<a href="/">Click to go back to Index</a></center></h1>'
            return HttpResponse(html)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponse("Logged In")
        else:
            return HttpResponse("<center><h1>Invalid Credentials Try Again<br>" + '<a href="/">Click to go back to Index</a></center></h1>')
