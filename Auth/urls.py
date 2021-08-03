from django.urls import path , include
from .views import *

app_name = "Auth"
urlpatterns= [
    path('users/login/', Login.as_view() , name='login')

]