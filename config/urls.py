from django.contrib import admin
from django.urls import path, include
from chart import views

urlpatterns = [
    path('', include('chart.urls')),
    path('world-population/',
         views.world_population, name='world_population'),
    path('admin/', admin.site.urls),
]