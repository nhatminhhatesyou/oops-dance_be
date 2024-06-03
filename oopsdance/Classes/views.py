from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.utils import timezone
from .serializers import ClassSerializer, ScheduleSerializer
from ..Attendance.serializers import AttendanceSerializer
from oopsdance.models import Class, ClassSchedule, Attendance

import datetime

from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    permission_classes
)

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
    
class ClassCountByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        try:
            class_count = Class.objects.filter(instructor_id=instructor_id).count()
            return Response({"instructor_id": instructor_id, "class_count": class_count}, status=status.HTTP_200_OK)
        except Class.DoesNotExist:
            return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([AllowAny])
class ClassesTodayByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        today = timezone.localtime().date()
        classes_today = Attendance.objects.filter(
            instructor_id=instructor_id,
            date = today
        ).distinct()

        serializer = AttendanceSerializer(classes_today, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class ClassesToday(APIView):
    def get(self, request, format=None):
        today = timezone.localtime().date()
        print(f"Today's date: {today}")
        classes_today = Attendance.objects.filter(
            date = today
        ).distinct()

        serializer = AttendanceSerializer(classes_today, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)