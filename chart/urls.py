from django.contrib import admin
from django.urls import path
from chart import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket-class/1/',
         views.ticket_class_view_1, name='ticket_class_view_1'),
    path('json-example/', views.json_example, name='json_example'),
    path('json-example/data/', views.chart_data, name='chart_data'),
    path('covid/', views.covid, name='covid'),
    path('covid19/', views.covid19, name='covid19'),
    path('admin/', admin.site.urls),
]