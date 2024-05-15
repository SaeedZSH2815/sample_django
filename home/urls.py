from django.urls import path
from . import views


urlpatterns = [
    path('home/home.html',view=views.home_page),
    path('todo_api_view',view=views.todo_json_apiView),
    path('home/alltodo_apiView',view=views.alltodo_apiView),
    path('home/',view=views.index_page),
    path('home/todo_details/<int:clID>',view=views.todo_details),
    #----------
    path()
]
