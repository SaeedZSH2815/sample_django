from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from . import models
from django.http import HttpRequest,JsonResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import TodoSerializer
from rest_framework.views import APIView
#mixins
from rest_framework import generics,mixins


# Create your views here.
#from django.conf.urls import url
#from rest_framework_swagger.views import get_swagger_view

#schema_view = get_swagger_view(title='Pastebin API')

# urlpatterns = [
#     url(r'^$', schema_view)
# ]


def home_page(request):
    lcontext= { 
                'message':"Ali",
                'message1':"saeed",
             
               }
    return render(request,'home/home.html',lcontext)


def index_page(request):
    lcontext={'todos':models.Todo.objects.order_by('priority').all()}
    return render(request,'home/index.html',lcontext)


def todo_json(request:HttpRequest):    
    lp =list(models.Todo.objects.all().values('title'))
    return JsonResponse({'todo':lp})

@api_view(['GET'])
def todo_json_apiView(request : Request):
    lp =list(models.Todo.objects.all().values('title','isdone'))
    return Response({'todo':lp},status=status.HTTP_200_OK)

@api_view(['GET'])
def alltodo_apiView(request : Request):
    if(request.method =='GET'):
      todolist =models.Todo.objects.order_by('priority').all()
      todolist_serializer = TodoSerializer(instance=todolist,many=True)
      try:
        return Response(todolist_serializer.data,status=status.HTTP_200_OK)
      except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    
#region 
@api_view(['GET','PUT','POST','DELETE'])
def todo_details(request : Request,clID : int):
      #todolist =models.Todo.objects.order_by('priority').all()[:1]
      #todolist : models.Todo  = models.Todo.objects.all().filter(id__exact=clID).first()
      #todolist  = models.Todo.objects.order_by("priority").all()[:2:1]
    try:

      todolist : models.Todo  = models.Todo.objects.all().get(pk=clID)
    except Exception as e:
      print(e)
      return Response(None,status=status.HTTP_400_BAD_REQUEST)

    if(request.method == 'GET'):
      todolist_serializer = TodoSerializer(instance=todolist,many=False)     
      return Response(todolist_serializer.data,status=status.HTTP_200_OK)  
    
    
    if(request.method == 'PUT'):
      todolist_serializer = TodoSerializer(instance=todolist,data=request.data,many=False)     
      if(todolist_serializer.is_valid()):
       todolist_serializer.save()
       return Response(todolist_serializer.data,status=status.HTTP_200_OK)  
    
    
    
    if(request.method == 'POST'):
      todolist_serializer = TodoSerializer(data=request.data,many=False)     
      if(todolist_serializer.is_valid()):
       todolist_serializer.save()
       return Response(todolist_serializer.data,status=status.HTTP_201_CREATED)  
         
    if(request.method == 'DELETE'):
       todolist.delete()
       return Response(None,status=status.HTTP_204_NO_CONTENT)  
#endregion    
    
#region APIView
class AllToDoAPIView(APIView):
  def get(self,clRequest : Request):
    LTodolist : models.Todo = models.Todo.objects.all()
    LTodoSerializer = TodoSerializer(instance=LTodolist,many=True)
    return Response(data=LTodoSerializer.data,status=status.HTTP_200_OK)
  
  def post(self,clRequest : Request):
    LTodo : TodoSerializer = TodoSerializer(data=clRequest.data,many=False)
    if LTodo.is_valid(raise_exception=True):
     LTodo.save() 
     return Response(data=LTodo.data,status=status.HTTP_201_CREATED)
    else:
      return Response(None,status=status.HTTP_400_BAD_REQUEST)
    
class GetToDoDetailAPIView(APIView):
  def getObject(self,id : int):
    try:
     LTodo : models.Todo = models.Todo.objects.get(pk=id)  
     return LTodo
    except Exception as EX:
     return None
    
  def get(self,clRequest : Request,clid : int):
    LTodo: models.Todo = self.getObject(id=clid)
    if (LTodo == None):
     return Response(data={"msg":"notFound","todo":None},status=status.HTTP_404_NOT_FOUND)   
    else:
     LTodoSerializer = TodoSerializer(instance=LTodo,many=False)
     return Response(data=LTodoSerializer.data,status=status.HTTP_200_OK)  
 
  def put(self,clRequest : Request,clid : int):
    LTodo: models.Todo = self.getObject(id=clid)
    LTodoSerializer = TodoSerializer(instance=LTodo,data=clRequest.data,many=False)
    if(LTodoSerializer.is_valid(raise_exception=True)):
     LTodoSerializer.save()     
     return Response(data=LTodoSerializer.data,status=status.HTTP_200_OK)
    else:
      return Response(None,status=status.HTTP_400_BAD_REQUEST)    
    
  def delete(self,clRequest : Request,clid : int):
    LTodo: models.Todo = self.getObject(id=clid)
    LTodo.delete()   
    return Response(None,status=status.HTTP_204_NO_CONTENT)    
#endregion

#region mixins
class AllToDoMixinsAPIView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
  queryset = models.Todo.objects.all()
  serializer_class = TodoSerializer
  
  def get(self,clRequest : Request):
    return self.list(request=clRequest)
  
  def post(self,clRquest : Request):
    return self.create(request=clRquest)
  
  
class DegToDoDetailMixinsAPIView(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
  queryset = models.Todo.objects.all()
  serializer_class = TodoSerializer
  
  def get(self,clRequest : Request,pk):
    return self.retrieve(request= clRequest,kwargs= pk) 

  
#endregion