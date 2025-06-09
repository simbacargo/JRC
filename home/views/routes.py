from django.views.decorators.cache import cache_page
from django.shortcuts import render
from time import sleep
from ..models import *

@cache_page(60 * 1)
def index(req):
    welcome_message:str = WelcomeMessage.objects.all().values("message")[0]["message"]
    print(welcome_message)
    context: dict[str:str] ={
        "welcome_message":welcome_message
    }
    welcome_message
    return render (req, "home.html",context)

@cache_page(60 * 1)
def beliefs(req):
    beliefs =Beliefs.objects.all()
    context = {
        "beliefs":beliefs
    }
    print(context)
    return render (req, "beliefs",context)

def about(req):
    return render (req, "about.html")

def calendar(req):
    return render (req, "Calendar/index.html")

def event(req):
    return render (req, "home.html")

@cache_page(60 * 1)
def upcoming_events(req):
    events = EventsHome.objects.all()
    print(events)
    return render (req, "Events/upcomming",{"events":events})

def event_details(req):
    return render (req, "home.html")

def sermons(req):
    return render (req, "Sermons/index.html")

def recent_sermons(req):
    return render (req, "Sermons/recent.html")

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