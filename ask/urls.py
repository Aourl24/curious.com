from django.contrib import admin
from django.urls import path
from .views import fview, Qfview, sview, pview,aview, pendview, searchview, notificationview,dark,likeV, \
like2view,answerView, imageView, answerDetailView


urlpatterns=[
    path('home',fview,name='HomeUrl'),
    path('home/<str:filter>/', fview, name='FilterUrl'),
    path('create/', Qfview, name= 'CreateUrl'),
    path('Q<int:id>/', sview,  name='QuestionUrl'), 
    path('like<int:id>/', likeV, name='lyk'),
    path('profile/<int:id>', pview, name='ProfileUrl'), 
    path('about/', aview, name='about'), 
    path('pend/', pendview, name='pend'), 
    path('search/', searchview, name='SearchUrl'),    
    path('notify/', notificationview, name='notify'),
    path('dark/', dark, name='darkmode'),
    path('<int:id>/', like2view, name='like'),
    path('<int:id>/answer',answerView,name='AnswerUrl'),
    path('<int:id>/answer<int:reply>/',answerView,name='AnswerReplyUrl'),
    path('<int:id>/image',imageView,name='ImageUrl'),
    path('<int:id>/answerdetail',answerDetailView,name='AnswerDetailUrl')
]