from django.urls import path, include
from .views import *

app_name = 'Form'
urlpatterns = [
    path('list/', FormList.as_view(), name="FormList"),
    path('form/new/', FormCreate.as_view(), name="FormCreate"),
    path('form/<int:pk>/edit/', FormUpdate.as_view(), name='FormUpdate'),
    path('form/<int:pk>/view/', FormView.as_view(), name='FormView'),

    path('question/new/text/<int:pk>/', TextQuestionCreate.as_view(), name='TextQuestionCreate'),
    path('question/new/optional/<int:pk>/', OptionalQuestionCreate.as_view(), name='OptionalQuestionCreate'),
]
