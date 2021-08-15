from django.urls import path, include
from .views import *

app_name = 'Employee'
urlpatterns = [
    path('employee/list/', EmployeeList.as_view(),name="EmployeeList"),
    path('employee/new/', EmployeeCreate.as_view(),name="EmployeeCreate"),
    path('employee/<int:pk>/view',EmployeeProfile.as_view(),name="EmployeeProfile"),
    path('employee/<int:pk>/edit' ,EmployeeUpdate.as_view(),name="EmployeeUpdate" ),
    path('employee/<int:pk>/delete/', EmployeeDelete.as_view(), name='EmployeeDelete'),


]

