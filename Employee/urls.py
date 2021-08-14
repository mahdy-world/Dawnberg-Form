from django.urls import path, include
from .views import *

app_name = 'Employee'
urlpatterns = [
    
    path('employee/new/', EmployeeCreate.as_view(),name="EmployeeCreate")

]

