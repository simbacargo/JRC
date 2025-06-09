
from django.contrib import admin
from django.urls import path, include
from home.views.more import *
from home.views.routes import *
urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
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
    path('api/recent-sermons', recent_sermons),
    path('api/beliefs', beliefs),
    path('api/upcoming_events', upcoming_events),
    path('api/upcoming_events', upcoming_events),
    path('api/upcoming_events', upcoming_events),
    path('api/upcoming_events', upcoming_events),
    path('api/upcoming_events', upcoming_events),
    path('api/upcoming_events', upcoming_events),

]



urlpatterns += [
    path('register_visit/', register_visit, name='register_visit'),
]
