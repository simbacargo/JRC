from django.shortcuts import render
from time import sleep
# Create your views here.
def index(req):
    return render (req, "home.html")

def about(req):
    return render (req, "about.html")

def calendar(req):
    return render (req, "Calendar/index.html")

def event_details(req):
    return render (req, "home.html")

def sermons(req):
    return render (req, "Sermons/index.html")

def sermons_details(req):
    return render (req, "home.html")

def contact(req):
    return render (req, "Contact.html")

def give(req):
    return render (req, "give.html")

def home(req):
    return render (req, "home.html")

def ministries(req):
    return render (req, "ministries.html")

def prayer_requests(req):
    return render (req, "home.html")

from django.http import JsonResponse,HttpResponse

def test(req):
    return HttpResponse('')