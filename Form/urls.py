from django.urls import path, include
from .views import *

app_name = 'Form'
urlpatterns = [
    path('form/list/', FormList.as_view(), name="FormList"),
    path('form/new/', FormCreate.as_view(), name="FormCreate"),
    path('form/<int:pk>/edit/', FormUpdate.as_view(), name='FormUpdate'),
    path('form/<int:pk>/view/', FormView.as_view(), name='FormView'),

    path('question/new/text/<int:pk>/', TextQuestionCreate.as_view(), name='TextQuestionCreate'),
    path('question/new/optional/<int:pk>/', OptionalQuestionCreate.as_view(), name='OptionalQuestionCreate'),
    path('question/edit/text/<int:pk>/', TextQuestionUpdate.as_view(), name='TextQuestionUpdate'),
    path('question/edit/option/<int:pk>/', OptionQuestionUpdate.as_view(), name='OptionQuestionUpdate'),
    path('question/<int:pk>/delete', QuestionDelete.as_view(), name='QuestionDelete'),

    path('form/answer/<int:pk>/', guest_form, name='guest_form'),
    path('form/answer/thankyou/', thank_you, name="thankyou"),

    path('form/<int:pk>/answer/list/', AnswerList.as_view(), name='AnswerList'),

    path('form/<int:pk>/add_call/', add_call, name='AddCall'),
    path('form/<int:pk>/view_call/', CallDetail.as_view(), name='CallDetail'),
    path('form/<int:pk>/update_call/', CallUpdate.as_view(), name='CallUpdate'),
    path('form/<int:pk>/add_comment/', add_comment, name='AddComment'),
    path('form/<int:pk>/update_comment/', CommentUpdate.as_view(), name='CommentUpdate'),
    path('form/<int:pk>/convert/', Convert.as_view(), name='Convert'),
    path('form/<int:pk>/change_status/', InstanceStatusUpdate.as_view(), name='InstanceStatusUpdate'),
    path('form/<int:pk>/assign_to_self/', assign_to_me, name='assign_to_self'),
    path('form/<int:pk>/delete/', delete_instance, name='delete_instance'),


    path('status/list/', StatusList.as_view(), name='StatusList'),
    path('status/create/', StatusCreate.as_view(), name='StatusCreate'),
    path('status/<int:pk>/update/', StatusUpdate.as_view(), name='StatusUpdate'),
    path('status/<int:pk>/delete/', StatusDelete.as_view(), name='StatusDelete'),

]
