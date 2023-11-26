from django.http import HttpResponse
from django.shortcuts import render


def start1(request):
    return render(request, "start1.html")

def start2(request):
    return render(request, "start2.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def userinfo(request):
    return render(request, "userinfo.html")

def choose(request):
    return render(request, "choose.html")

def allergy(request):
    return render(request, "allergy.html")

def indpref(request):
    return render(request, "indpref.html")