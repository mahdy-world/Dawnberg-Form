from django.urls import path, include
from .views import *

app_name = 'Employee'
urlpatterns = [
    path('employee/list/', EmployeeList.as_view(),name="EmployeeList"),
    path('profile/list/', ProfileList.as_view(),name="ProfileList"),
    path('employee/new/', EmployeeCreate.as_view(),name="EmployeeCreate"),
    path('employee/<int:pk>/view',EmployeeProfile.as_view(),name="EmployeeProfile"),
    path('employee/<int:pk>/edit' ,EmployeeUpdate.as_view(),name="EmployeeUpdate" ),
    path('employee/<int:pk>/delete/', EmployeeDelete.as_view(), name='EmployeeDelete'),
    path('employee/<int:pk>/user/create/', create_user_employee, name='create_user_employee')

]

