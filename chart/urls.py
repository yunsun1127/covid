from django.contrib import admin
from django.urls import path
from chart import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket-class/1/',
         views.ticket_class_view_1, name='ticket_class_view_1'),
    path('covid/', views.covid, name='covid'),
    path('covid19/', views.covid19, name='covid19'),
    path('admin/', admin.site.urls),
]