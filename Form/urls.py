from django.urls import path , include
from .views import *

app_name = 'Form'
urlpatterns = [
    path('list/',FormList.as_view(),name="FromList"),
    path('form/new/',FormCreate.as_view() , name="FormCreate")
]
