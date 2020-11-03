from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *


def index(request):
    return render(request, 'package.html')
