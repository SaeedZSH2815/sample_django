from django.urls import path
from . import views




urlpatterns = [
   
    path('home/home.html',view=views.home_page),
    path('todo_api_view',view=views.todo_json_apiView),
    path('alltodo_apiView',view=views.alltodo_apiView),
    path('',view=views.index_page),
    path('todo_details/<int:clID>',view=views.todo_details),
    #----------
    path('AllToDoAPIView',view=views.AllToDoAPIView.as_view()),
    path('GetToDoDetailAPIView/<int:clid>',view=views.GetToDoDetailAPIView.as_view()),
    #mixins
    path('AllToDoMixinsAPIView',view=views.AllToDoMixinsAPIView.as_view()),
    path('DegToDoDetailMixinsAPIView/<pk>',view=views.DegToDoDetailMixinsAPIView.as_view()),
]
