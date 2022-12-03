from collections import deque
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import get_user_model

from .models import Task
from .serializers import *
from .renderers import *

User = get_user_model()

# Create your views here.
class ListTasksView(APIView):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Task.objects.filter(userId=request.user.id)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTaskView(APIView):
    serializer_class = CreateTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.context["user_id"] = request.user.id
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'success', 'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': 'something went wrong', 'data': e}, status=status.HTTP_201_CREATED)



class EditTaskView(APIView):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        taskId = request.data.get('taskId')
        name = request.data.get('name')
        desc = request.data.get('description')
        status = request.data.get('status')
        due_date = request.data.get('due_date')

        task = Task.objects.get(id=taskId)
        task.name = name
        task.description = desc
        task.status = status
        task.due_date = due_date
        task.userId = request.user.id
        task.save()

        return Response({'status': 'success', 'msg': 'Task updated successfully'})



class DeleteTaskView(APIView):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        
        taskId = request.data.get('taskId')
        try:
            task = Task.objects.get(id=taskId)
            task.delete()
            return Response({'status': 'success', 'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            
