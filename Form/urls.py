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
    path('question/edit/text/<int:pk>/', TextQuestionUpdate.as_view(), name='TextQuestionUpdate'),
    path('question/edit/option/<int:pk>/', OptionQuestionUpdate.as_view(), name='OptionQuestionUpdate'),


    
    path('form/answer/<int:pk>/', guest_form, name='guest_form'),
    path('form/answer/thankyou/', thank_you , name="thankyou"),
    path('form/<int:pk>/answer/list/', AnswerList.as_view(), name='AnswerList'),

    path('form/<int:pk>/add_call/' , add_call ,name='AddCall'),
    path('form/<int:pk>/update_call/', CallUpdate.as_view() , name='CallUpdate'),

    path('form/<int:pk>/add_comment/' , add_comment ,name='AddComment'),
    path('form/<int:pk>/update_comment/', CommentUpdate.as_view() , name='CommentUpdate'),

    path('form/<int:pk>/convert/' , Convert.as_view() , name='Convert'),
    path('form/<int:pk>/take/',take, name='Take'),
    

]

