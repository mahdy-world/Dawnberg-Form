from django.urls import path , include
from .views import *

app_name = "Branch"
urlpatterns= [
    path('branch/list/', BranchList.as_view(),name="BranchList"),
    path('branch/new/', BranchCreate.as_view(),name="BranchCreate"),
    path('branch/<int:pk>/edit/' , BranchUpdate.as_view(),name="BranchUpdate"),
    path('branch/<int:pk>/delete/', BranchDelete.as_view(), name='BranchDelete'),
 


]