
from django.contrib import admin
from django.urls import path
from home.views.more import *
from home.views.routes import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('about', about),
    path('calendar', calendar),
    path('calendar/details/<pk>', event_details),
    path('sermons', sermons),
    path('sermons/details/<pk>', sermons_details),
    path('contact', contact),
    path('give', give),
    path('home', home),
    path('ministries', ministries),
    path('prayer_requests', prayer_requests),
    path('test', test),
]



urlpatterns += [
    path('register_visit/', register_visit, name='register_visit'),
]
