from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import ClassSerializer, ScheduleSerializer
from oopsdance.models import Class, ClassSchedule

class AddClassView(APIView):
    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClassListView(APIView):
    def get(self, request, format=None):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    
class ClassDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    
class ScheduleListView(APIView):
    def get(self, request, format=None):
        schedule = ClassSchedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)
    
class AddScheduleView(APIView):
    def post(self, request, format=None):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class ScheduleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleSerializer