from django.urls import path , include
from . import views

app_name = 'Core'
urlpatterns = [
    path('', views.Index, name='index')
]
